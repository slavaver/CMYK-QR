# Репозиторий проекта «Маркировка изображений»

## Установка

В проекте используется Anaconda и менеджер пакетов Conda.

Для создания среды и установки трубуемых пакетов используйте requirements.txt.

`$ conda create --name <env> --file requirements.txt`

Pillow устанавливается через pip, так как в conda для pillow не включен imagingcms, который работает с LittleCMS (lcms2).

## TODO

- Изменить принцип поиска qr кода
- Проверить правильность get_qr_coordinates из analisis.py