# Personalized Movie Recommender
## Краткое описание

[![Build Status](https://travis-ci.com/fotol1/pers_obj_rec.svg?branch=master)](https://travis-ci.org/fotol1/pers_obj_rec)
 [![codecov](https://codecov.io/gh/fotol1/pers_obj_rec/branch/master/graph/badge.svg)](https://codecov.io/gh/fotol1/pers_obj_rec)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Репозиторий содержит проект, выполненный в рамках курса "Архитектура, дизайн и процесс разработки ПО". Реализация выполнена на `Python3.6` с помощью фреймворка `Flask`.

Проект представляет из себя веб-сервис, с помощью которого можно получить персонализированную подборку фильмов. Подборка формируется исходя из интересов пользователя, которые он может выразить положительной оценкой фильмов, которые предлагаются сервисом. Чем больше пользователь оставит обратной связи о фильмах, тем точнее будет работать ранжирование.

Ранжирование осуществляется с помощью моделей машинного обучения. Модели располагаются в директории `recommenders`. Кроме модели, которая ранжирует фильмы случайным образом, остальные модели требуют обучения. Для обучения достаточно предоставить разреженную матрицу с бинарными (implicit) данными.
1 будет означать то, что соответствующий (строке) пользователь выразил предпочтение соответствующему (колонке) фильму. Пропущенные значения заполняются нулями. Такой подход является общепринятым.

В случае если пользователь вообще не выразил предпочтений, но уже зарегистрировался, модель все равно ранжирует фильмы исходя из их популярности.

Так как сама по себе рекомендация может оказаться бесполезной, то на сайте также можно выбрать кинотеатр и получить персональную подборку именно в выбранном месте. С точки зрения алгоритма, происходит фильтрация по фильмам, которые на данный момент доступны в кинотеатре. Данные об этом содержатся в сущности `app.models.Items_in_Provider`. Так как фильмы в кинотеатрах показываются в течение какого-то определенного времени, то экземпляры этой сущности имеют дату начала и дату конца. Если дата конца неизвестна, то ей выставляется бесконечно большое время. В процессе выдачи доступных фильмов, находятся только те, которые показываются в кинотеатре в текущий момент времени.

Начиная с версии 0.2.1 добавлены пользователи из датасета Movielens 100k. Каждый из пользователей имеет зарегисрированную учетную запись на сайте, в базе данных хранятся их интеракции. Это сделано для того, чтобы наполнить сайт какими-то данными, и чтобы рекомендации фильмов для реальных пользователей были осмыслены. Подробнее о датасете:

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets:
History and Context. ACM Transactions on Interactive Intelligent
Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages.
DOI=http://dx.doi.org/10.1145/2827872

## Установка и запуск

Проект обернут в `Docker`. Для запуска достаточно выполнить `./docker_update.sh`. Команда установит необходимые зависимости и запустит приложение локально. В веб-браузере будет доступен по адресу http://0.0.0.0:5000

Также версия 0.2.1 доступна по адресу http://fotol.pythonanywhere.com/

## Тестирование

`python3 -m unittest discover`
