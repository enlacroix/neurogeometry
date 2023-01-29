# neurogeometry
## Как пользоваться?
Запуск через файл main.py, редактирование условия задачи через data_task.py - меняем массив input_info и переменную question.
Ознакомиться с предикатной "азбукой" можно в файле book.txt. 
## Структура проекта

+ predmain, fixpred, quadpred, freepred, objpred:
Cодержат описание классов, которые образуют предикатную логику. 
+ entities.py: 
Содержит классы линий, углов, треугольников, **объектов**, которые могут быть аргументами предикатов.
+ parameters.py:
Скудные (пока что) настройки. 
+ extmethods.py:
содержит минорные функции, которые используются при тестировке.
+ printer.py
отвечает за внешний вид выводимого решения, "декоратор". 
+ geom.csv:
дедуктивный датафрейм - результат работы алгоритма. Строками датафрейма является структура вида 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'.
+ prototype.py:
интерфейс-пустышка, выполненный на Streamlit. Для тех кому было интересно. Так должен выглядеть зимний прототип. 
+ rules.py:
сборник теорем(правил), которыми владеет программа. Сейчас залито штук 10, остальные пока тестирую на предмет багов. **Именно поэтому** модель имеет ограниченную работоспособность. 
+ solver.py:
алгоритм, который решает задачу по прямому *методу перенасыщения*, когда уже ничего нового извлечь нельзя из задачи, то он останавливается. 
+ statement.py:
здесь храним глобальные переменные - предикаты, точки, датафрейм, доступные всем файлам проекта.
+ testing.py:
черновики, боль, отчаяние. Несущественный файл с предыдущими алгоритами точечного поиска. 
## Азбука предикатов
Предикат - некая функция от точек, которая отражает ту или иную геометрическую взаимосвязь между ними.
+ col(...): точки-аргументы лежат на одной прямой.
+ cyl(...): точки лежат на одной окружности.
+ mdp(X, Y, Z): точка Х - середина отрезка YZ. 
+ cir(X, ...): X - центр окружности, на которой лежат точки ...
+ prl(A, B, C, D): AB параллелен CD.
+ eql(A, B, C, D): AB = CD.
+ ort(A, B, C, D): AB перпендикулярен CD.
+ eqa(A, B, C, D, P, Q, F, H): ∠[AB, CD] = ∠[PQ, FH], равенство углов.
+ ctr(A, B, C, D, P, Q): равные треугольники ABC и DPQ.  
