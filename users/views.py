from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm

@login_required
def dashboard(request):
    user = request.user

    # Fetch all transactions
    incomes = Income.objects.filter(user=user)
    expenses = Expense.objects.filter(user=user)

    # Total calculations
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    savings = total_income - total_expense

    # Forms
    if request.method == 'POST':
        if 'income_submit' in request.POST:
            i_form = IncomeForm(request.POST)
            if i_form.is_valid():
                new_income = i_form.save(commit=False)
                new_income.user = user
                new_income.save()
                return redirect('dashboard')
        elif 'expense_submit' in request.POST:
            e_form = ExpenseForm(request.POST)
            if e_form.is_valid():
                new_expense = e_form.save(commit=False)
                new_expense.user = user
                new_expense.save()
                return redirect('dashboard')
    else:
        i_form = IncomeForm()
        e_form = ExpenseForm()

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'i_form': i_form,
        'e_form': e_form,
    }
    return render(request, 'users/dashboard.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')
