from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,DeleteView
from django.views.decorators.http import require_POST
from django.shortcuts import resolve_url,redirect
from django.http import HttpResponse
from .models import Expence,Revenue,Category_in,Category_out
from .forms import ExpenceCreate,ExpenceUpdate,RevenueCreate,RevenueUpdate
import datetime,io
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
font = {"family":"IPAexGothic"}
matplotlib.rc('font', **font)

# Create your views here.
User = get_user_model()

# 家計簿
class List(LoginRequiredMixin,TemplateView):
    template_name = 'money/list.html'
    
    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']

        expence = Expence.objects.filter(user=user,date__year=year,date__month=month).order_by('date')
        
        context['expence_lists'] = expence if len(expence) else None

        revenue = Revenue.objects.filter(user=user,date__year=year,date__month=month).order_by('date')

        context['revenue_lists'] = revenue if len(revenue) else None

        context['year'] = year
        context['month'] = month
        context['prev_year'] = year-1 if month==1 else year
        context['prev_month'] = month-1 if month>1 else 12
        context['next_year'] = year+1 if month==12 else year
        context['next_month'] = month+1 if month<12 else 1

        sum_ex = 0
        for e in expence:
            sum_ex += e.cost

        context['sum_ex'] = sum_ex

        sum_re = 0
        for r in revenue:
            sum_re += r.cost

        context['sum_re'] = sum_re

        context['sum'] = sum_re - sum_ex

        expenceMonthly(user,year,month)
        revenueMonthly(user,year,month)

        return context

# 新規支出作成
class NewExpence(LoginRequiredMixin,CreateView):
    model = Expence
    form_class = ExpenceCreate
    template_name = 'money/new_expence.html'

    def get_initial(self):
        user = self.request.user.pk
        return {'user':user,}

    def get_success_url(self):
        form = ExpenceCreate(self.request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            return resolve_url('money:list',year=date.year,month=date.month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        context["year"] = int(now.year)
        context["month"] = int(now.month)

        return context
    

# 支出変更画面
class ExpenceUpdate(LoginRequiredMixin,UpdateView):
    model = Expence
    template_name = 'money/expence_update.html'
    form_class = ExpenceUpdate

    def get_success_url(self):
        user = self.request.user
        expence = Expence.objects.filter(user=user, pk=self.kwargs['pk'])
        year = expence[0].date.year
        month = expence[0].date.month
        return resolve_url("money:list", year=year,month=month)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        expence = Expence.objects.filter(user=user, pk=self.kwargs['pk'])
        context["year"] = expence[0].date.year
        context["month"] = expence[0].date.month
        return context

# 支出削除
def DeleteExpence(request, pk):
    user = request.user
    expence = Expence.objects.filter(user=user, pk=pk)
    year = expence[0].date.year
    month = expence[0].date.month
    expence[0].delete()
    return redirect('money:list', year=year,month=month)

# 新規収入作成
class NewRevenue(LoginRequiredMixin,CreateView):
    model = Revenue
    template_name = 'money/new_revenue.html'
    form_class = RevenueCreate

    def get_initial(self):
        user = self.request.user.pk
        return {'user':user,}

    def get_success_url(self):
        form = RevenueCreate(self.request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            return resolve_url('money:list',year=date.year,month=date.month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        context["year"] = int(now.year)
        context["month"] = int(now.month)

        return context
    

# 収入変更画面
class RevenueUpdate(LoginRequiredMixin,UpdateView):
    model = Revenue
    template_name = "money/revenue_update.html"
    form_class = RevenueUpdate

    def get_success_url(self):
        user = self.request.user
        revenue = Revenue.objects.filter(user=user, pk=self.kwargs['pk'])
        year = revenue[0].date.year
        month = revenue[0].date.month

        return resolve_url('money:list', year=year,month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        revenue = Revenue.objects.filter(user=user, pk=self.kwargs['pk'])
        context["year"] = revenue[0].date.year
        context["month"] = revenue[0].date.month

        return context
    
# 収入削除
def DeleteRevenue(request,pk):
    user = request.user
    revenue = Revenue.objects.filter(user=user, pk=pk)
    year = revenue[0].date.year
    month = revenue[0].date.month
    revenue[0].delete()

    return redirect('money:list', year=year, month=month)
    
# グラフ作成

# svgの変換
# def pltToSvg():
#     buf = io.BytesIO()
#     plt.savefig(buf,format='svg', bbox_inches='tight')
#     s = buf.getvalue()
#     buf.close()
#     return s

# 支出月内訳の円作成
def expenceMonthly(user, year, month):
    data = Expence.objects.filter(user=user, date__year=year, date__month=month)
    label = []
    x = []
    
    for c in Category_out.objects.all():
        expence = data.filter(category=c.id)
        sum_ = 0
        for e in expence:
            sum_ += int(e.cost)
        if sum_ > 0: 
            x.append(sum_)
            label.append(c.name)

    # 背景色をhtmlに合わせる
    fig = plt.figure()
    plt.pie(x,labels=label)
    fig.savefig("./static/images/expence_{}_{}.svg".format(year,month),transparent=True)

# 収入月内訳の円作成
def revenueMonthly(user,year,month):
    data = Revenue.objects.filter(user=user, date__year=year, date__month=month)
    label = []
    x = []
    
    for c in Category_in.objects.all():
        revenue = data.filter(category=c.id)
        sum_ = 0
        for r in revenue:
            sum_ += int(r.cost)
        if sum_ > 0: 
            x.append(sum_)
            label.append(c.name)

    # 背景色をhtmlに合わせる
    fig = plt.figure()
    plt.pie(x,labels=label)
    fig.savefig("./static/images/revenue_{}_{}.svg".format(year,month),transparent=True)



# def expenceSvg(request,year,month):
#     user = request.user
#     expenceMonthly(user,year,month)
#     svg = pltToSvg()
#     plt.cla()
#     response = HttpResponse(svg, content_type='image/svg+xml')
#     return response

# def revenueSvg(request,year,month):
#     user = request.user
#     revenueMonthly(user,year,month)
#     svg = pltToSvg()
#     plt.cla()
#     response = HttpResponse(svg, content_type='image/svg+xml')
#     return response



    