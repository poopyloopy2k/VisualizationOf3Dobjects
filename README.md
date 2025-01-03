# 3D Object Transformation Web Application

Этот проект представляет собой веб-приложение для выполнения трехмерных преобразований объектов. Приложение позволяет масштабировать, вращать и переносить объекты, а также отображать результаты в 3D и различных ортографических проекциях. Реализовано с использованием Flask и Plotly.

## Функциональность

Приложение реализует следующие функции:

- **Масштабирование**: Применяет масштабирование объекта в 3D пространстве.
- **Вращение**: Реализует вращение объекта вокруг осей X, Y и Z.
- **Перенос**: Выполняет перемещение объекта в 3D пространстве по осям X, Y и Z.
- **Отображение преобразованного объекта**:
  - **3D график**: Показывает 3D модель объекта с использованием библиотеки Plotly.
  - **Ортографические проекции**: Отображает проекции объекта на плоскости XY, XZ и YZ.
- **Матрица преобразования**: Выводит итоговую матрицу, которая используется для применения выбранных преобразований.

## Установка

1. Убедитесь, что у вас установлен Python 3.6 или выше.
2. Склонируйте репозиторий на ваш компьютер:
   ```bash
   git clone https://github.com/poopyloopy2k/VisualizationOf3Dobjects.git
   cd VisualizationOf3Dobjects

   
 3. Установите необходимые библиотеки:
```bash```
Копировать код
 ```pip install -r requirements.txt```
Запустите приложение:
bash
Копировать код
python app.py
Перейдите в браузер по адресу http://127.0.0.1:5000/ для взаимодействия с приложением.


## Использование
При загрузке страницы вам будет предложено ввести параметры для масштабирования, вращения (углы в градусах для осей X, Y, Z) и переноса (по осям X, Y, Z).
Нажмите кнопку для отображения преобразованного объекта в 3D и получения его ортографических проекций.
Итоговая матрица преобразования будет отображена на экране.
 ## Вклад
Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк и отправьте pull request. Мы приветствуем любые улучшения и исправления.

## Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь с нами по адресу: likholap.fedor@gmail.com.
