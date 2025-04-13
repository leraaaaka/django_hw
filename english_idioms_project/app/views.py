import random
from django.shortcuts import render
from django import forms

from .models import Idiom


def home(request):
    return render(request, 'home.html')


def random_idiom_view(request):
    # Получим все идиомы из базы
    idioms = Idiom.objects.all()
    if not idioms.exists():
        # Если база пуста
        context = {
            'idiom': None,
            'message': "В базе пока нет идиом. Добавьте в админке."
        }
        return render(request, 'random_idiom.html', context)
    
    # Выбираем случайную
    random_idiom = random.choice(idioms)
    
    context = {
        'idiom': random_idiom
    }
    return render(request, 'random_idiom.html', context)


class QuizForm(forms.Form):
    question_idiom_id = forms.IntegerField(widget=forms.HiddenInput())
    choice = forms.IntegerField(
        label='Выберите правильный вариант',
        widget=forms.RadioSelect,
        required=True
    )

def quiz_view(request):
    # Если POST (ответ на вопрос), проверяем ответ
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            question_id = form.cleaned_data['question_idiom_id']
            selected_id = form.cleaned_data['choice']
            try:
                correct_idiom = Idiom.objects.get(id=question_id)
                chosen_idiom = Idiom.objects.get(id=selected_id)
            except Idiom.DoesNotExist:
                return render(request, 'quiz_result.html', {
                    'message': "Ошибка: выбранная идиома не найдена."
                })
            
            # Проверяем: совпадает ли выбранный вариант с правильным
            if chosen_idiom.id == correct_idiom.id:
                message = "Верно! Вы выбрали правильное значение для «{}».".format(correct_idiom.phrase)
            else:
                message = "Неверно! Правильный ответ для «{}» – это «{}».".format(
                    correct_idiom.phrase, correct_idiom.definition[:70] + '...'
                )
            return render(request, 'quiz_result.html', {
                'message': message
            })
        else:
            return render(request, 'quiz_result.html', {
                'message': "Форма не прошла валидацию."
            })
    
    # Если GET – генерируем новый вопрос
    idioms = Idiom.objects.all()
    total = idioms.count()
    if total < 4:
        return render(request, 'quiz.html', {
            'error': "Недостаточно идиом в базе (нужно >= 4) для теста."
        })
    
    # 1) Случайная идиома (правильный ответ)
    correct_idiom = random.choice(idioms)
    # 2) Несколько других для ложных вариантов
    #    (убираем correct_idiom, чтобы не дублировать)
    others = idioms.exclude(id=correct_idiom.id)
    # выбираем 3 случайные записи (или 2, на ваш выбор)
    wrong_options = random.sample(list(others), 2)
    
    # Формируем список всех вариантов (правильный + ложные)
    all_options = wrong_options + [correct_idiom]
    random.shuffle(all_options)
    
    # Создаём форму
    form = QuizForm()
    # Сохраняем ID правильной идиомы для проверки
    form.fields['question_idiom_id'].initial = correct_idiom.id
    
    # Подготовим данные для RadioSelect
    # choice – это IntegerField, а в качестве вариантов возьмём (id, definition)
    CHOICES = [(idiom.id, idiom.definition[:70] + '...') for idiom in all_options]
    form.fields['choice'].widget.choices = CHOICES
    
    context = {
        'form': form,
        'correct_idiom': correct_idiom,
        'options': all_options
    }
    return render(request, 'quiz.html', context)
