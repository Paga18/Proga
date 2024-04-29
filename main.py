from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import cv2

# Глобальные переменные для громкости музыки и эффектов
music = 0
effects = 0
# Глобальные переменные для количества строк и столбцов
rows = 5
cols = 5
# Флаги размытия, чб эффекта и нумерации прямоугольников
blur_check = 0
grey_check = 0
num_check = 0
# В track передаётся саундтрек. Сделал его глобальным, чтобы музыка играла в любой части меню
track = SoundLoader.load('soundtrack.mp3')
sound = SoundLoader.load('click_sound.mp3')


# Класс интерактивной картинки
class InteractiveImage(Widget):
    def __init__(self, image_path, **kwargs):
        super(InteractiveImage, self).__init__(**kwargs)
        # Количество строк и столбцов, путь к картинке
        self.rows = rows
        self.cols = cols
        self.image_path = image_path
        # Массив прямоугольников
        self.rectangles = []
        # Инициализация изображения и отрисовка прямоугольников
        self.init_image()
        self.draw_rectangles()

    def init_image(self):
        # Здесь рисуем холст, его фоном становится наша картинка, изменения размеров окна не приветствуется
        # так как в качестве размера берём размер окна, а не самой картинки
        self.img = cv2.imread(self.image_path)
        bl = 200
        self.ksize = (bl, bl)
        self.img = cv2.resize(self.img, Window.size)
        #   cv2.imwrite("resized.jpg", self.img)
        self.img = cv2.blur(self.img, self.ksize, cv2.BORDER_DEFAULT)

        h, w, _ = self.img.shape
        h = h // self.rows
        w = w // self.cols
        for j in range(self.cols):
            for i in range(self.rows):
                piece = self.img[i * h:(i + 1) * h, j * w:(j + 1) * w]
                cv2.imwrite(f'pieces/piece_{i}_{j}.jpg', piece)

        with self.canvas:
            self.bg = Rectangle(source=self.image_path, pos=self.pos, size=Window.size)
            self.size = Window.size

    # Функция отрисовки прямоугольников
    def draw_rectangles(self):
        with self.canvas:
            for col in range(self.cols):
                for row in range(self.rows):
                    # Color(random(), random(), random(), 1)  # Прозрачный цвет для секций
                    rect = Rectangle(pos=((self.width / self.cols) * col, (self.height / self.rows) * row),
                                     size=(self.width / self.cols, self.height / self.rows),
                                     source=f'pieces/piece_{self.rows - row - 1}_{col}.jpg')
                    self.rectangles.append(rect)

    # Функция, привязанная к нажатию на экран
    def on_touch_down(self, touch):
        super(InteractiveImage, self).on_touch_down(touch)
        # Проверка того, что нажатие внутри изображения

        # if self.collide_point(*touch.pos):
        # Ширина столбца и высота строки считается как ширина и высота окна делить на их количество
        col_width = Window.size[0] / self.cols
        row_height = Window.size[1] / self.rows
        # номер удаляемого прямоугольника вычисляется как координаты нажатия
        # по х делить на ширину и по y делить на высоту
        col = int(touch.x // col_width)
        row = int(touch.y // row_height)
        index = col * self.rows + row
        # Удаляем этот прямоугольник
        try:
            self.canvas.remove(self.rectangles[index])
        except:
            pass


# Главное меню игры
class MainMenu(BoxLayout):
    sound.volume = effects / 100  # Изначальная громкость эффектов
    track.volume = music / 100    # Изначальная громкость музыки
    track.loop = True             # Когда музыка закончится, она начнёт играть заново
    track.play()                  # Запуск музыки

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        # my_image вынесена в __init__ для проверки пути файла во внешней функции
        self.my_image = None
        # Вызов функции главного меню. Туда передаётся 0 по приколу, так как прога требует аргумент
        self.open_menu(0)

    # Функция для звука нажатия на кнопку
    def btn_pressed(self, instance):
        global effects
        global sound
        sound.volume = effects / 100
        sound.play()

    # Функция главного меню
    def open_menu(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()

        # Добавление фона
        with self.canvas:
            rect = Rectangle(source='background_image1.jpg', size=Window.size)

        # "Кнопка" для красивой надписи, мол сделано нами
        info_text = Button(text='created by 306Team',
                           background_color=(0, 0, 0, 0),
                           color=(0, 0, 0, 1),
                           font_name="397-font.otf",
                           font_size="14sp")
        # Настройка окружения для красивых кнопок
        self.orientation = 'vertical'
        self.size_hint = (0.35, 0.65)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.37}
        self.spacing = 15

        # Создание кнопок
        play_button = Button(text='Играть',
                             background_color=(0, 220 / 255, 20 / 255, 1),  # Цвет фона кнопки
                             color=(1, 1, 1, 1),  # Цвет текста на кнопке
                             font_name="397-font.otf",  # Шрифт
                             font_size="40sp",  # Размер шрифта
                             background_normal='',  # Эти два параметра нужны для того, чтобы фон
                             background_down='',    # не влиял на цвет кнопки
                             on_press=self.btn_pressed)  # Вызов функции звука нажатия на кнопку
        settings_button = Button(text='Настройки',
                                 background_color=(0, 220 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)
        exit_button = Button(text='Выход',
                             background_color=(1, 40 / 255, 50 / 255, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)
        # Пустая кнопка, чтобы сделать отступ для text_info
        empty_button = Button(background_color=(0, 0, 0, 0))

        # Здесь мы привязываем нажатия кнопок к функциям
        play_button.bind(on_press=self.select_image)
        settings_button.bind(on_press=self.open_settings)
        exit_button.bind(on_press=self.exit_game)

        # А здесь добавляем эти кнопки в приложение
        self.add_widget(play_button)
        self.add_widget(settings_button)
        self.add_widget(exit_button)
        self.add_widget(empty_button)
        self.add_widget(info_text)

    # Функция для выбора изображения
    def select_image(self, instance):
        # Очищаем экран от всего
        self.clear_widgets()

        # Задаём размеры и позицию виджетов
        self.size_hint = (0.5, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.spacing = 15

        info_text = Button(text='Выберите изображение',
                           background_color=(0, 0, 0, 0),
                           color=(0, 0, 1 / 2, 1),
                           font_name="397-font.otf",
                           font_size="40sp",
                           size_hint=(1, 0.05))
        # BoxLayout - это структура, которая может в себе содержать несколько кнопок/изображений/ползунков и тд.
        # Мы задаём здесь 2 BoxLayout'а, так как в одной структуре нельзя иметь как горизонтальные,
        # так и вертикальные объекты.
        hbox1 = BoxLayout(orientation="horizontal",
                          size_hint=(1.5, 0.5),
                          pos_hint={'center_x': 0.5, 'center_y': 0.8})
        hbox2 = BoxLayout(orientation="horizontal",
                          size_hint=(1.5, 0.08),
                          pos_hint={'center_x': 0.5, 'center_y': 0.1},
                          spacing=500)

        self.my_image = Image(fit_mode="scale-down")  # Параметр нужен для того, чтобы изображение не растягивалось
        filechooser = FileChooserIconView(filters=["*.jpg", "*.png"],  # Фильтр файлов
                                          font_name='397-font.otf')    # Шрифт
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)
        continue_button = Button(text='Продолжить',
                                 background_color=(0, 220 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)

        filechooser.bind(selection=self.selected)
        exit_button.bind(on_press=self.open_menu)
        continue_button.bind(on_press=self.select_rows_cols)

        hbox1.add_widget(self.my_image)
        hbox1.add_widget(filechooser)
        hbox2.add_widget(exit_button)
        hbox2.add_widget(continue_button)

        self.add_widget(info_text)
        self.add_widget(hbox1)
        self.add_widget(hbox2)

    # Функция для выбора строк/столбцов и афинных преобразований
    def select_rows_cols(self, instance):
        if self.my_image.source is None:
            # Если пользователь не выбрал файл, то вылезает окошко, которое не позволит пройти дальше
            # и попросит пользователя выбрать изображение
            exit_button = Button(text='Понятно',
                                 background_color=(0, 220 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)
            popup = Popup(size_hint=(0.4, 0.3),
                          content=exit_button,
                          title='Ошибка! Выберите изображение',
                          title_color=(1, 1, 1, 1),
                          title_font='397-font.otf',
                          title_size='28sp',
                          separator_color=(0, 0, 0, 0))
            popup.open()
            exit_button.bind(on_press=lambda *args: popup.dismiss())

        else:
            global rows, cols
            self.clear_widgets()

            self.size_hint = (0.5, 1)
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.spacing = 75

            info_text = Button(text='Выберите параметры',
                               background_color=(0, 0, 0, 0),
                               color=(0, 0, 1 / 2, 1),
                               font_name="397-font.otf",
                               font_size="40sp",
                               size_hint=(1, 0.1),
                               pos_hint={'center_x': 0.5, 'center_y': 1.7})

            hbox1 = BoxLayout(orientation="horizontal",
                              size_hint=(1.5, 0.05),
                              pos_hint={'center_x': 0.5, 'center_y': 0.75},
                              spacing=50)
            blur_button = Button(text='Размытие: выкл.',
                                 background_color=(1, 20 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="28sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed,
                                 on_release=self.change_blur)
            grey_button = Button(text='Монохром: выкл.',
                                 background_color=(1, 20 / 255, 20 / 255, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="28sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed,
                                 on_release=self.change_grey)
            numbering_button = Button(text='Нумерация: выкл.',
                                      background_color=(1, 20 / 255, 20 / 255, 1),
                                      color=(1, 1, 1, 1),
                                      font_name="397-font.otf",
                                      font_size="28sp",
                                      background_normal='',
                                      background_down='',
                                      on_press=self.btn_pressed,
                                      on_release=self.change_numbering)
            # Все эти if/else нужны для сохранения состояния кнопок
            if blur_check == 1:
                blur_button.text = 'Размытие: вкл.'
                blur_button.background_color = (0, 220 / 255, 20 / 255, 1)
            else:
                blur_button.text = 'Размытие: выкл.'
                blur_button.background_color = (1, 20 / 255, 20 / 255, 1)

            if grey_check == 1:
                grey_button.text = 'Монохром: вкл.'
                grey_button.background_color = (0, 220 / 255, 20 / 255, 1)
            else:
                grey_button.text = 'Монохром: выкл.'
                grey_button.background_color = (1, 20 / 255, 20 / 255, 1)

            if num_check == 1:
                numbering_button.text = 'Нумерация: вкл.'
                numbering_button.background_color = (0, 220 / 255, 20 / 255, 1)
            else:
                numbering_button.text = 'Нумерация: выкл.'
                numbering_button.background_color = (1, 20 / 255, 20 / 255, 1)

            rows_layout = BoxLayout(orientation='horizontal',
                                    size_hint=(1, 0.05),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})
            # "Кнопка", в которую передаётся значение количества строк
            rows_input = Button(text=f'Строки: {rows}',
                                background_color=(0, 1 / 4, 1, 1),
                                color=(1, 1, 1, 1),
                                font_name="397-font.otf",
                                font_size="28sp",
                                background_normal='',
                                background_down='')
            # Ползунок для строк
            slider_rows = Slider(min=1, max=10, value=rows,  # Минимальное, максимальное и изначальное значения
                                 background_width="30sp",  # Ширина полоски
                                 value_track=True,  # Нужно для отслеживания ползунка
                                 value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                                 cursor_size=(50, 40),  # Размер курсора ползунка
                                 cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                                 step=1)  # Шаг от 1 до 10 только по целым числам
            slider_rows.bind(value=self.update_value_row)

            cols_layout = BoxLayout(orientation='horizontal',
                                    size_hint=(1, 0.05),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.4})
            # "Кнопка", в которую передаётся значение количества столбцов
            cols_input = Button(text=f'Столбцы: {cols}',
                                background_color=(0, 1 / 4, 1, 1),
                                color=(1, 1, 1, 1),
                                font_name="397-font.otf",
                                font_size="28sp",
                                background_normal='',
                                background_down='')
            # Ползунок для столбцов
            slider_cols = Slider(min=1, max=10, value=cols,
                                 background_width="30sp",
                                 value_track=True,
                                 value_track_color=[1, 1 / 2, 0, 1],
                                 cursor_size=(50, 40),
                                 cursor_image="cursor.png",
                                 step=1)
            slider_cols.bind(value=self.update_value_col)

            hbox2 = BoxLayout(orientation="horizontal",
                              size_hint=(1.5, 0.05),
                              pos_hint={'center_x': 0.5, 'center_y': 0},
                              spacing=500)
            start_button = Button(text='Начать игру',
                                  background_color=(0, 220 / 255, 20 / 255, 1),
                                  color=(1, 1, 1, 1),
                                  font_name="397-font.otf",
                                  font_size="40sp",
                                  background_normal='',
                                  background_down='',
                                  on_press=self.btn_pressed)
            exit_button = Button(text='Назад',
                                 background_color=(1, 1 / 2, 0, 1),
                                 color=(1, 1, 1, 1),
                                 font_name="397-font.otf",
                                 font_size="40sp",
                                 background_normal='',
                                 background_down='',
                                 on_press=self.btn_pressed)

            start_button.bind(on_press=self.launch_game)
            exit_button.bind(on_press=self.select_image)

            rows_layout.add_widget(rows_input)
            rows_layout.add_widget(slider_rows)
            cols_layout.add_widget(cols_input)
            cols_layout.add_widget(slider_cols)

            hbox1.add_widget(blur_button)
            hbox1.add_widget(grey_button)
            hbox1.add_widget(numbering_button)

            hbox2.add_widget(exit_button)
            hbox2.add_widget(start_button)

            self.add_widget(info_text)
            self.add_widget(hbox1)
            self.add_widget(rows_layout)
            self.add_widget(cols_layout)
            self.add_widget(hbox2)

    # Включение/выключение блюра
    def change_blur(self, instance):
        global blur_check
        if blur_check == 1:
            instance.text = 'Размытие: выкл.'
            instance.background_color = (1, 20 / 255, 20 / 255, 1)
            blur_check = 0
        else:
            instance.text = 'Размытие: вкл.'
            instance.background_color = (0, 220 / 255, 20 / 255, 1)
            blur_check = 1

    # Включение/выключение чб эффекта
    def change_grey(self, instance):
        global grey_check
        if grey_check == 1:
            instance.text = 'Монохром: выкл.'
            instance.background_color = (1, 20 / 255, 20 / 255, 1)
            grey_check = 0
        else:
            instance.text = 'Монохром: вкл.'
            instance.background_color = (0, 220 / 255, 20 / 255, 1)
            grey_check = 1

    # Включение/выключение хз чего, пока что не придумали
    def change_numbering(self, instance):
        global num_check
        if num_check == 1:
            instance.text = 'Нумерация: выкл.'
            instance.background_color = (1, 20 / 255, 20 / 255, 1)
            num_check = 0
        else:
            instance.text = 'Нумерация: вкл.'
            instance.background_color = (0, 220 / 255, 20 / 255, 1)
            num_check = 1

    # Функция для изменения значения строк
    def update_value_row(self, instance, value):
        global rows
        label = instance.parent.children[1]  # Получаем Label
        rows = int(value)
        label.text = f'Строки: {rows}'

    # Функция для изменения значения столбцов
    def update_value_col(self, instance, value):
        global cols
        label = instance.parent.children[1]  # Получаем Label
        cols = int(value)
        label.text = f'Столбцы: {cols}'

    # Переменная obj - это filechooser; val - массив с выбранными файлами.
    # Выбираем val[0], так как это первый выбранный пользователем файл
    def selected(self, obj, val):
        try:
            self.my_image.source = val[0]
        except:
            pass

    # Функция, привязанная к кнопке "Начать игру"
    def launch_game(self, instance):
        # Очищаем экран от всего
        self.clear_widgets()
        self.spacing = 0
        # И открываем нашу интерактивную картинку, передаём имя файла, столбцы и строки
        self.add_widget(InteractiveImage(self.my_image.source))

    # Функция для отображения настроек
    def open_settings(self, instance):
        # Очищаем окно от предыдущих кнопок и тд
        self.clear_widgets()
        self.orientation = 'vertical'

        # Установка новых параметров, чтобы были красивые кнопки
        self.size_hint = (0.35, 0.4)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # "Кнопка", в которую передаётся значение количества строк

        music_layout = BoxLayout(orientation='horizontal')
        effects_layout = BoxLayout(orientation='horizontal')

        music_button = Button(text=f'Музыка: {music}%',
                              background_color=(0, 1 / 4, 1, 1),
                              color=(1, 1, 1, 1),
                              font_name="397-font.otf",
                              font_size="26sp",
                              background_normal='',
                              background_down='')
        # Ползунок для строк
        slider_music = Slider(min=0, max=100, value=music,  # Минимальное, максимальное и текущее значения
                              background_width="30sp",  # Ширина полоски
                              value_track=True,  # Нужно для отслеживания ползунка
                              value_track_color=[1, 1 / 2, 0, 1],  # Цвет закрашенной полоски
                              cursor_size=(50, 40),  # Размер курсора ползунка
                              cursor_image="cursor.png",  # Курсор есть картинка, здесь передаётся какая именно
                              step=1)  # Шаг от 1 до 100 только по целым числам

        effects_button = Button(text=f'Эффекты: {effects}%',
                                background_color=(0, 1 / 4, 1, 1),
                                color=(1, 1, 1, 1),
                                font_name="397-font.otf",
                                font_size="26sp",
                                background_normal='',
                                background_down='')
        slider_effects = Slider(min=0, max=100, value=effects,
                                background_width="30sp",
                                value_track=True,
                                value_track_color=[1, 1 / 2, 0, 1],
                                cursor_size=(50, 40),
                                cursor_image="cursor.png",
                                step=1)
        # Кнопка "Назад"
        exit_button = Button(text='Назад',
                             background_color=(1, 1 / 2, 0, 1),
                             color=(1, 1, 1, 1),
                             font_name="397-font.otf",
                             font_size="40sp",
                             background_normal='',
                             background_down='',
                             on_press=self.btn_pressed)

        # Здесь мы привязываем нажатия кнопок/ползунков к функциям
        slider_music.bind(value=self.update_value_music)
        slider_effects.bind(value=self.update_value_effects)
        exit_button.bind(on_press=self.open_menu)

        # Здесь добавляется всё, что было описано выше
        music_layout.add_widget(music_button)
        music_layout.add_widget(slider_music)
        effects_layout.add_widget(effects_button)
        effects_layout.add_widget(slider_effects)

        self.add_widget(music_layout)
        self.add_widget(effects_layout)
        self.add_widget(exit_button)

    # Функция для изменения значения громкости музыки
    def update_value_music(self, instance, value):
        global music
        label = instance.parent.children[1]  # Получаем Label
        music = int(value)
        track.volume = music / 100
        label.text = f'Музыка: {music}%'

    # Функция для изменения значения громкости эффектов
    def update_value_effects(self, instance, value):
        global effects
        label = instance.parent.children[1]  # Получаем Label
        effects = int(value)
        sound.volume = effects / 100
        label.text = f'Эффекты: {effects}%'

    # Функция выхода из игры
    def exit_game(self, instance):
        App.get_running_app().stop()


class GameApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    GameApp().run()
