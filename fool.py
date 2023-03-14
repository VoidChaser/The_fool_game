import itertools
import os
import random
import sys
from functools import total_ordering

import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)

# Инициализируем экран и модуль пайгейм

numses = {'нет': 0,
          '1': 1,
          '2': 2,
          '3': 3,
          '4': 4,
          '5': 5,
          '6': 6,
          '7': 7,
          '8': 8,
          '9': 9,
          '10': 10,
          'валет': 11,
          'дама': 12,
          'король': 13,
          'туз': 14}

suits = ['пик', 'черви', 'буби', 'крести']
nums = ['6', '7', '8', '9', '10', 'валет', 'дама', 'король', 'туз']
start_deck = [a for a in itertools.product(nums, suits)]


# Инициализируем фундамент системы карт - масти и достоинства карт(цифры), а также формируем стартовую колоду,
# из которой потом будем делать все остальные колоды.


def start_screen():
    intro_text = ["Представляю вам Карточную игру Дурак.",
                  "",
                  "Правила типичны, колода 36 карт, без джокеров,",
                  "В начале игры:",
                  "",
                  "Происходит перемешивание колоды.",
                  "На каждого игрока выдается 6 карт, при раздаче определеятся козырная масть.",
                  "**В качестве козыря при раздаче не ставятся тузы.**",
                  "P.s. Карты козырной масти ценятся в игре, так как любая карта козырной масти может",
                  "покрыть любую карту кроме козырных карт достоинством выше.",
                  "!!!Иногда слетает текст, особенность прорисовки в пайгейм. Если видите,",
                  "что текст поехал при запуске, перезапустите игру.!!!!!",
                  "Определение первого хода:",
                  "Первый ход определяется наличием козырей у игроков,",
                  " и/или их достоинством: у кого есть карта козырной масти",
                  "наивысшего достоинства, тот и ходит первым.",
                  "Правило определения первого хода работает при условии того,",
                  " что игроки начинают новый матч, в котором никто не успел проиграть;",
                  "Иначе, первым ходит тот, кто проиграл.",
                  "",
                  "При атаке:",
                  "Во время игры игроки по очереди выкладывают карты, атакуя друг-друга по-очереди.",
                  "Атака происходит любой картой из своей колоды",
                  "В ответ защищающийся игрок должен отбить карту противника картой козырной масти,",
                  "либо высшего достоинства",
                  "Но атаковать после первого раза, когда отбили карту,"
                  "можно только картами такого же достоинства",
                  "В противном случае, защищающийся обязан взять все оставшиеся карты со стола,",
                  " или взять сразу первую карту, если не может её отбить.",
                  "Защита происходит до того момента, как на столе окажутся 6 заверщенных пар карт,",
                  " - игроки останутся без карт, либо игрок в защите возьмёт карты, или отобъется.",
                  "После каждого хода игроки добирают карты до 6. Игрок, который атаковал берёт карты первый.",
                  "Если в конце игры оба игрока не могут полно добрать карты, то карты делятся пополам,",
                  " так, что больше карт достается тому, кто ходил последним."]

    screen = pygame.display.set_mode((800, 800))
    fon = pygame.transform.scale(load_image('sukno.jpg'), (800, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

    # Создаём заставку


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
    # Описываем функцию загрузки изображений


class Card:
    def __init__(self, num, suit):
        super().__init__()
        self.suit = suit
        self.str_num = num
        self.num = self.get_num()
        self.kozir = False  # Чтобы инициализировать когда козырь определен конкретную масть - тру

        # Опишем в инициализаторе класса Card инициализацию по масти и номеру

    def __repr__(self):
        return f'Карта {self.str_num} {self.suit}'

    def __str__(self):
        return f'{self.str_num} {self.suit}'

    def __eq__(self, other):
        if self.kozir:
            if other.kozir:
                if self.num == other.num:
                    return True

        elif not self.kozir:
            if not other.kozir:
                if self.suit == other.suit:
                    if self.num == other.num:
                        return True
            return False
        # Ретёрн прерывает выполнение функции. Когда условие выполняется - выполнение прервется на значении - тру,
        # в остальных значениях, - фолс.

    def __lt__(self, other):
        if self.kozir:
            if other.kozir:
                if self.num < other.num:
                    return True

        elif not self.kozir:
            if other.kozir:
                return True
            elif not other.kozir:
                if self.suit == other.suit:
                    if self.num < other.num:
                        return True

        return False

    def __ge__(self, other):
        if self.kozir:
            if other.kozir:
                if self.num > other.num:
                    return True

        elif not self.kozir:
            if other.kozir:
                return False
            elif not other.kozir:
                if self.suit == other.suit:
                    if self.num > other.num:
                        return True

        return False

    # Описываем методы сравнения

    def get_num(self):
        return numses[self.str_num]

    # метод получения истинного числового значения для карты - карта валет - истинное значение - 11, и т д.

    def __hash__(self):
        return hash(self.num)
    # Описываем метод hash для сравнения экземпляров в словарях


No_cards = Card('нет', 'козырей')
ruba = load_image('рубашка.png')
blank_image = load_image('blank_sprite.png')
bito_card_image = load_image('рубашка_боком.png')
# Инициализируем изображения, которые потому бедем использовать.

FPS = 50
ATTACKING_Y = 300
CARD_WIDTH = 100
DEFENDING_Y = 375
X_POS_MULTIPLIER = 150
HOD_X = 250
PC_FOOL_COUNT = 0
PLAYER_FOOL_COUNT = 0

# Инициализируем константы.

clock = pygame.time.Clock()

background_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
bito_sprites = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()


# Инициализируем группы спрайтов.


@total_ordering
class Hand:
    def __init__(self, name):
        self.name = name
        self.container = []
        self.hod = None
        self.count_cards = None
        self.kozirs_count = None
        self.lowest_kozir = None

    # Описываем инициализатор класса Hand

    def pop(self, index):
        item_to_ret = self.container.pop(index)
        return item_to_ret

    # Описываем метод pop

    def recount(self):
        global kozir
        self.count_cards = len(self.container)
        count = 0
        high_num = 16
        lowest_card = No_cards
        for _ in self.container:
            if _.suit == game.kozir.suit:
                if _.num < high_num:
                    high_num = _.num
                    lowest_card = _
                count += 1
        self.kozirs_count = count
        self.lowest_kozir = lowest_card

    # Описываем метод пересчёта колоды - пересчёта и переустановления значений самой высшей козырной карты, а также
    def __iadd__(self, other):
        self.container += [other]
        self.container = sorted(list(set(self.container)), key=lambda x: (x.suit, x.num))
        self.recount()
        return self

    def __eq__(self, other):
        if self.container == other.container:
            return True
        else:
            return False

    def __le__(self, other):
        if self.kozirs_count:
            if other.kozirs_count:
                if self.lowest_kozir < other.lowest_kozir:
                    return True
                else:
                    return False
            else:
                return False

        elif not self.kozirs_count:
            if other.kozirs_count:
                return True
            elif not self.kozirs_count:
                return False

        # Описываем два основных метода сравнения для того,
        # чтобы итертулс декоратор их дописал. Учитываем,
        # что начинает та рука, у которой козырь меньше, либо наличествует.

    def __delitem__(self, key):
        del self.container[key]

    def __len__(self):
        return len(self.container)

    def __getitem__(self, item):
        return self.container[item]

    def __index__(self, element):
        return self.container.index(element)

    def index(self, element):
        return self.container.index(element)

    def __iter__(self):
        return iter(self.container)

    def pop(self, index):
        to_pop_item = self.container.pop(index)
        return to_pop_item

    def __repr__(self):
        return f"Колода {self.name}: Карт: {len(self.container)}, карты: " + ', '.join(list(
            map(str, self.container))) + f', Козырей: {self.kozirs_count}, Наименьший козырь: {self.lowest_kozir}'

    # Описываем остальные методы, необходимые для функционирования колоды


class Card_sprite(pygame.sprite.Sprite):
    def __init__(self, card: Card, x, y, show=False):
        super().__init__(card_sprites)
        self.card = card
        self.shown = show
        self.card_image = load_image(f'{self.card}.png')
        self.update()
        self.rect = self.card_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        card.image = self

    def show_card(self):
        self.shown = not self.shown

    def update(self, new_coords=None):
        if self.shown:
            self.image = self.card_image

        else:
            self.image = ruba

        if new_coords:
            self.rect.x, self.rect.y = new_coords

    def __repr__(self):
        return f'Спрайт карты {self.card}'

    # Описываем класс спрайтов карт


class Cloth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(background_sprites)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.image.fill(pygame.Color('#41ac43'))

    # Описываем класс спрайта полотна


class Bito_sprite(pygame.sprite.Sprite):
    def __init__(self, card: Card, x, y):
        super().__init__(bito_sprites)
        self.card = card

        self.update(card)
        self.rect.x = x
        self.rect.y = y

    def update(self, new_img=None):
        if new_img:
            if type(new_img) is Card:
                self.image = load_image(f'{self.card}.png')
                self.rect = self.image.get_rect()

            if type(new_img) is pygame.Surface:
                self.image = new_img
                self.rect = self.image.get_rect()

    # Описываем класс спрайтов колоды.


class Button_sprite(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font_size=40):
        super().__init__(button_sprites)
        self.text = text
        self.font_size = font_size
        self.x, self.y = x, y

        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render(self.text, False, (pygame.Color(255, 255, 255)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.update()

    def update(self, new_text=None):
        if new_text is not None:
            self.text = new_text
            self.image = self.font.render(self.text, False, (pygame.Color(255, 255, 255)))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x - self.rect.width // 2, self.y - self.rect.height // 2

    # Описываем спрайт класса кнопок.


class Interface_Sprite(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font_size=25):
        super().__init__(interface_sprites)
        self.text = text
        self.font_size = font_size
        self.x, self.y = x, y

        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render(self.text, False, (pygame.Color(255, 255, 255)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.update()

    def update(self, new_text=None):
        if new_text is not None:
            self.text = new_text
        self.image = self.font.render(self.text, False, (pygame.Color(255, 255, 255)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    # Описываем класс спрайтов надписей


class Game:
    def __init__(self):
        self.previlege_hod_user = None
        self.first_round_user = None
        # self.allowed_cards = []
        self.hodit = None
        self.winner = None
        self.pc_hand = None
        self.player_hand = None
        self.all_hod_used_cards = []
        self.hands = []
        self.deck = []
        self.kozir = None
        self.hod_dict = {}
        self.hod = 0
        self.win = False
        self.game_name = Interface_Sprite('Дурак by tr', 330, 5)
        self.pc_hand_name = Interface_Sprite('Колода Pc', 30, 30, font_size=30)
        self.player_hand_name = Interface_Sprite('Колода Player', 15, 570, font_size=30)
        self.bito_button = Button_sprite('Бито', 850, 250)
        self.take_button = Button_sprite('Беру', 850, 460)
        self.make_new_game_button = Button_sprite('', 500, 400)
        self.deck_cards_count = Interface_Sprite('', 935, 315)
        self.log_sprite = Interface_Sprite('', 15, 750)
        self.kozir_sprite = None
        self.bito_sprite = None
        # self.kozir_while_empty_value = None
        self.kozir_while_empty_suit = Interface_Sprite(f'Козыри:', 820, 335)
        self.kozir_while_empty_value = Interface_Sprite(f'', 820, 355)
        self.cloth = Cloth()

        # Инициализируем атрибуты класса

    def draw_cards_who_played(self):
        if self.hod_dict:
            keys, values = list(self.hod_dict.keys()), list(
                filter(lambda x: x is not None, list(self.hod_dict.values())))
            if self.first_round_user == 'Pc':
                for _ in range(len(values)):
                    values[_].image.update(((X_POS_MULTIPLIER * (_ + 1)) - CARD_WIDTH - 15, DEFENDING_Y))
                for _ in range(len(keys)):
                    keys[_].image.update(((X_POS_MULTIPLIER * (_ + 1)) - CARD_WIDTH, ATTACKING_Y))

            else:
                for _ in range(len(values)):
                    values[_].image.update(((X_POS_MULTIPLIER * (_ + 1)) - CARD_WIDTH - 15, ATTACKING_Y))
                for _ in range(len(keys)):
                    keys[_].image.update(((X_POS_MULTIPLIER * (_ + 1)) - CARD_WIDTH, DEFENDING_Y))

    # Метод рисует карты при их выкладе.

    def new_game(self):
        self.winner = None
        if self.hands:
            self.hands = []
        self.flop_deck_to_hands()
        self.begin_round(first_hod=True)
        self.deck_cards_count.update(str(len(game.deck)))
        self.log_sprite.update('')
        self.kozir_sprite = Bito_sprite(game.kozir, 820, 290)
        self.bito_sprite = Bito_sprite(bito_card_image, 850, 335)
        # self.kozir_while_empty_value = Interface_Sprite(f'', 820, 355)
        self.kozir_while_empty_suit.update(f'Козыри:')
        self.kozir_while_empty_value.update(f'{self.kozir.suit}', )

        self.win = False

    # Метод начинает новую игру

    def flop_deck_to_hands(self):
        self.deck = []
        for _ in range(len(start_deck)):
            card = Card(start_deck[_][0], start_deck[_][1])
            self.deck.append(card)

        shuffle_counter = random.randint(16, 30)
        for _ in range(shuffle_counter):
            random.shuffle(self.deck)

        kozir_pos = 12
        self.kozir = self.deck[kozir_pos]
        while self.kozir.num == 'туз':
            kozir_pos += 1
            self.kozir = self.deck[kozir_pos]

        for _ in self.deck:
            if _.suit == self.kozir.suit:
                _.kozir = True

        self.deck.pop(self.deck.index(self.kozir))
        self.deck.insert(0, self.kozir)

        pc_hand = Hand('Pc')
        player_hand = Hand('Player')

        self.add_decks(pc_hand, player_hand)
        self.pc_hand = pc_hand
        self.player_hand = player_hand
        for _ in range(6):
            self.pc_hand += self.deck.pop()
            self.player_hand += self.deck.pop()
        for _ in self.hands:
            _.recount()
        # print(f'Раздал карты первый раз.')

    # Метод раздаёт карты когда начинается игра и инициализирует козырь, руки игроков

    def get_index_user_name(self, pos=-1):
        if not self.hod_dict:
            return None

        last_dict_hod = list(self.hod_dict.keys())[pos]
        return self.get_involved_hand(last_dict_hod).name

        # Изменил возвращаемое значение функции на именно имя ключа из словаря, как имени пользователя, а не значения.

    def get_last_user_name(self):
        return self.get_index_user_name()

    def get_first_user_name(self):
        return self.get_index_user_name(0)

    def add_decks(self, *args):
        self.hands.extend(args)

    def init_and_draw_decks(self):
        for _ in self.hands:
            _.recount()
        y = 60
        for hand in self.hands:
            for _, it_card in enumerate(hand):
                if hand.name == 'Player':
                    Card_sprite(it_card, 5 + _ * WIDTH // hand.count_cards, y,
                                show=True)
                else:
                    Card_sprite(it_card, 5 + _ * WIDTH // hand.count_cards, y)
            y += 540
        # print()

    # Метод рисует карты в руках

    def dobor(self):
        first_taker = self.first_round_user
        if first_taker is not None:
            first_taker_hand = list(filter(lambda x: x.name == self.first_round_user, self.hands))[0]
            second_taker_hand = list(filter(lambda x: x.name != first_taker, self.hands))[0]
            if self.deck:
                while len(first_taker_hand) < 6 and self.deck:
                    first_taker_hand += self.deck.pop()
                    if len(game.deck) == 1:
                        bito_sprites.empty()
                        self.kozir_sprite = Bito_sprite(game.kozir, 820, 290)
                    # print('Убрал спрайт карты бито')
                    if self.kozir in first_taker_hand:
                        self.kozir_sprite.update(new_img=blank_image)
                        # print('Убрал спрайт козыря')
                while len(second_taker_hand) < 6 and self.deck:
                    second_taker_hand += self.deck.pop()
                    if len(game.deck) == 1:
                        bito_sprites.empty()
                        self.kozir_sprite = Bito_sprite(game.kozir, 820, 290)
                        # print('Убрал спрайт карты бито')

                    if self.kozir in second_taker_hand:
                        self.kozir_sprite.update(new_img=blank_image)
                        # print('Убрал спрайт козыря')
                self.deck_cards_count.update(str(len(self.deck)) if len(self.deck) else '')

                # Тут нужно учесть то, что в бито спрайтс еще будут карты, которые до козыря были.
                # И их тоже надо реализовать, как убираются. То есть, когда остаётся только один козырь при "брать",
                # убирать спрайт повёрнутой карты.
                # Метод добирает карты из колоды, смотрит,
                # нет ли победителя, и в зависимости от количества карт убирает спрайты колоды.

    def check_win(self):
        if not self.deck:
            wined_deck = list(filter(lambda x: len(x) == 0, self.hands))
            if wined_deck:
                self.win = True
                self.make_new_game_button.update('Начать новую игру')
                self.winner = wined_deck[0].name
                self.losed = list(filter(lambda x: x.name != self.winner, self.hands))[0]
                self.log_sprite.update(f'{self.winner} победил. {self.losed.name} остаётся в дураках.')
                return wined_deck[0]

    # Метод проверяет победу и возвращает имя если есть победитель.

    def begin_round(self, first_hod=False):
        self.all_hod_used_cards = []
        self.dobor()
        for _ in self.hands:
            _.recount()
        card_sprites.empty()
        self.init_and_draw_decks()
        self.winner = self.check_win()
        if self.winner:
            return
        self.hod_dict = {}
        if not first_hod:
            self.hodit = list(filter(lambda x: x != self.hodit, self.hands))[0]
            # print(f"Ходит: {self.hodit.name}")
        else:
            self.hodit = max(self.hands)
            self.previlege_hod_user = self.hodit
            # print(f"Первым ходит {self.hodit.name}:")
        self.first_round_user = self.hodit.name

    # Метод начинает новый раунд. Вызывается когда было бито или беру.

    def take(self, hand: Hand):
        for _ in self.all_hod_used_cards:
            used_hand = game.get_involved_hand(_)
            if used_hand != hand:
                used_hand.pop(used_hand.index(_))
            hand += _
        for _ in self.hands:
            _.recount()
        # self.hod_dict = {}
        # self.all_hod_used_cards = []

        # print(hand)
        # Сделать проверку на то, что карты нет в той руке, куда добавляем. - готово.

    # Метод беру.

    def bito(self):
        if self.all_hod_used_cards:
            for _ in game.hands:
                _.container = list(
                    filter(lambda x: x not in self.all_hod_used_cards, _.container))
                _.recount()
        # self.hod_dict = {}
        self.all_hod_used_cards = []

    # Метод бито.

    # Метод атаковать картой.

    def attack_card(self, attack_card: Card):
        if self.hodit.name == 'Player':
            taken_card_sprite = self.player_hand[self.player_hand.container.index(attack_card)].image
        else:
            taken_card_sprite = self.pc_hand[self.pc_hand.container.index(attack_card)].image
            taken_card_sprite.show_card()
        self.hod_dict[attack_card] = None
        taken_card_sprite.update()

    # Метод защищаться картой.

    def defend_card(self, defending_card: Card):
        if self.hodit.name != 'Player':
            defending_card.image.show_card()
        self.hod_dict[list(self.hod_dict.keys())[-1]] = defending_card
        defending_card.image.update()

    def get_involved_hand(self, card):
        return list(filter(lambda x: card in x, self.hands))[0]
    # Метод смотрит в какой руке находится карта.


def terminate():
    pygame.quit()
    sys.exit()


def formated_hod_return():
    return f'Сейчас ходит: {game.hodit.name}'


if __name__ == '__main__':
    pygame.display.set_caption('The fool')
    start_screen()
    # Пускаем заставку и после растягиваем экран.
    screen = pygame.display.set_mode((1000, 800))

    # game_name = Interface_Sprite('Дурак by tr', 330, 5)
    # pc_hand_name = Interface_Sprite('Колода Pc', 30, 30, font_size=30)
    # player_hand_name = Interface_Sprite('Колода Player', 15, 570, font_size=30)
    # bito_button = Button_sprite('Бито', 850, 250)
    # take_button = Button_sprite('Беру', 850, 460)
    # make_new_game_button = Button_sprite('', 500, 400)
    # cloth = Cloth()

    # Инициализируем спрайты, которые не используют данные, полученные в ходе игры.

    game = Game()
    game.new_game()

    # Инициализуем игру и начинаем новую игру.

    # deck_cards_count = Interface_Sprite(str(len(game.deck)), 935, 315)
    # log_sprite = Interface_Sprite('', 15, 750)
    # kozir_sprite = Bito_sprite(game.kozir, 820, 290)
    # bito_sprite = Bito_sprite(bito_card_image, 850, 335)

    # Создаём классы, которые используют данные, полученные в ходе игры.

    game.begin_round(first_hod=True)
    running = True

    # Начинаем раунд и начинаем running

    # Пока проект не доделан заставка закомментирована.

    while running:
        # while not game.win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # Поправил потому что последняя карта это та, которую будут класть,
            # в иных случаях надо смотреть на первую карту.
            # Fair play - Нужен чтобы смотреть, корректное ли действие, относительно правил сделал пользователь.

            if not game.win:
                fair_play = True
                game.all_hod_used_cards = [*list(game.hod_dict.keys()), *list(game.hod_dict.values())]
                game.all_hod_used_cards = list(filter(lambda x: x is not None, game.all_hod_used_cards))
                if game.hodit.name == 'Player':
                    founded = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        curr_x, curr_y = event.pos
                        _: Card_sprite
                        pushed_cards = list(filter(lambda x: (x.rect.x <= curr_x <= x.rect.x + x.rect.width) and (
                                x.rect.y <= curr_y <= x.rect.y + x.rect.height), card_sprites))
                        pushed_buttons = list(filter(lambda x: (x.rect.x <= curr_x <= x.rect.x + x.rect.width) and (
                                x.rect.y <= curr_y <= x.rect.y + x.rect.height), button_sprites))
                        if pushed_cards or pushed_buttons:
                            founded = True

                        if pushed_buttons:
                            shot_button = pushed_buttons[0]
                            button_text = shot_button.text
                            if button_text == 'Бито':
                                if game.first_round_user == 'Player':
                                    if game.all_hod_used_cards:
                                        game.log_sprite.update('Игрок говорит бито.')
                                        game.bito()
                                        game.begin_round()
                                    else:
                                        game.log_sprite.update(
                                            'Вы не можете сейчас говорить бито, потому что не положили ни одной карты.')
                                        fair_play = False
                                else:
                                    game.log_sprite.update(
                                        'Вы не можете сейчас говорить бито, потому что не вы атаковали первым.')
                                    fair_play = False
                                game.check_win()

                            elif button_text == 'Беру':
                                if game.first_round_user == 'Pc':
                                    game.log_sprite.update(f'Игрок берёт.')
                                    game.take(game.player_hand)
                                    game.begin_round()
                                else:
                                    game.log_sprite.update('Вы не можете брать сейчас, потому что вы ходите.')
                                    fair_play = False
                                game.check_win()

                        if pushed_cards:
                            shot_card = max(pushed_cards, key=lambda x: x.rect.x).card
                            # if shot_card == game.kozir:
                            #     pass
                            # else:
                            shot_deck_name = game.get_involved_hand(shot_card).name
                            if shot_deck_name == 'Player':
                                if game.first_round_user == 'Player' or game.first_round_user is None:
                                    if shot_card not in game.all_hod_used_cards:
                                        if not game.all_hod_used_cards:
                                            game.attack_card(shot_card)
                                            game.check_win()
                                        else:
                                            if shot_card.num in list(map(lambda x: x.num,
                                                                         game.all_hod_used_cards)) and shot_card not in game.all_hod_used_cards:
                                                game.attack_card(shot_card)
                                                game.check_win()
                                            else:
                                                game.log_sprite.update(
                                                    f'Картой {shot_card} '
                                                    f'нельзя атаковать, так как она не сходна по достоинству с уже'
                                                    f' выложенными картами.')
                                                fair_play = False
                                        if fair_play:
                                            game.log_sprite.update(f'Игрок атакует картой {shot_card}.')
                                    else:
                                        game.log_sprite.update(f'Картой {shot_card} уже ходили.')
                                        fair_play = False
                                    # Если первым ходил, игрок, то в раунде игрок будет только атаковать.
                                elif game.first_round_user == 'Pc':
                                    pc_played_card = list(game.hod_dict.keys())[-1]
                                    if shot_card not in game.all_hod_used_cards:
                                        if shot_card > pc_played_card:
                                            game.defend_card(shot_card)
                                            game.log_sprite.update(
                                                f'Игрок защищается от {pc_played_card} картой {shot_card}.')
                                            game.check_win()
                                        else:
                                            game.log_sprite.update(f'Этой картой нельзя защититься.'
                                                                   f' Она меньше по значению либо не подходит по масти.')
                                            fair_play = False
                                    else:
                                        game.log_sprite.update(f'Картой {shot_card} уже ходили.')
                                        fair_play = False
                            else:
                                game.log_sprite.update('Вы не выбрали вашу карту')
                                fair_play = False
                        if founded and not game.win:
                            if fair_play:
                                game.check_win()

                                # log_sprite.update('Игрок сходил')
                                # print(f'Состояние раунда на данный момент: {game.hod_dict}')
                                game.hodit = list(filter(lambda x: x.name != 'Player', game.hands))[0]
                    game.draw_cards_who_played()
                else:
                    if game.first_round_user == 'Pc' or game.first_round_user is None:
                        if game.pc_hand:
                            if not game.all_hod_used_cards:
                                cards_to_attacks = list(
                                    filter(lambda x: x not in game.all_hod_used_cards, game.pc_hand))
                            else:
                                cards_to_attacks = list(filter(lambda x: (x not in game.all_hod_used_cards) and (
                                        x.num in list(map(lambda y: y.num, game.all_hod_used_cards))),
                                                               game.pc_hand))
                            if cards_to_attacks:
                                not_kozired_cards_to_attack = list(
                                    filter(lambda x: x.suit != game.kozir.suit and x.num <= 11, cards_to_attacks))
                                if not_kozired_cards_to_attack:
                                    card_to_attack = not_kozired_cards_to_attack[
                                        random.randint(0, len(not_kozired_cards_to_attack) - 1)]
                                else:
                                    card_to_attack = min(cards_to_attacks)

                                game.attack_card(card_to_attack)
                                game.log_sprite.update(f'Компьютер атакует картой {card_to_attack}.')
                            else:
                                game.log_sprite.update(f'Компьютер говорит бито.')
                                game.bito()
                                game.begin_round()
                        else:
                            game.draw_cards_who_played()
                            game.check_win()

                    elif game.first_round_user == 'Player':
                        if game.player_hand:
                            # print(game.hod_dict)
                            player_played_card = list(game.hod_dict.keys())[-1]
                            possible_cards_to_defend = list(
                                filter(lambda x: x > player_played_card and x not in game.all_hod_used_cards,
                                       game.pc_hand))
                            if possible_cards_to_defend:
                                card_to_defend = min(possible_cards_to_defend)
                                game.defend_card(card_to_defend)
                                game.log_sprite.update(
                                    f'Компьютер защищается от {player_played_card} картой {card_to_defend}.')
                            else:
                                game.take(game.pc_hand)
                                game.log_sprite.update(f'Компьютер берёт.')
                                game.begin_round()
                        else:
                            game.check_win()

                    game.hodit = list(filter(lambda x: x.name != 'Pc', game.hands))[0]
                    game.draw_cards_who_played()
                game.check_win()

            if game.win:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    curr_x, curr_y = event.pos
                    pushed_buttons = list(filter(lambda x: (x.rect.x <= curr_x <= x.rect.x + x.rect.width) and (
                            x.rect.y <= curr_y <= x.rect.y + x.rect.height), button_sprites))
                    if pushed_buttons:
                        pushed_button = pushed_buttons[0]
                        if pushed_button.text == 'Начать новую игру':
                            if game.winner == 'Pc':
                                PLAYER_FOOL_COUNT += 1
                                if 2 <= PLAYER_FOOL_COUNT % 10 <= 4 and PLAYER_FOOL_COUNT // 10 % 2 == 0:
                                    game.player_hand_name.update(f'Колода Player, дурак {PLAYER_FOOL_COUNT} раза.')
                                else:
                                    game.player_hand_name.update(f'Колода Player, дурак {PLAYER_FOOL_COUNT} раз.')

                            elif game.winner == 'Player':
                                PC_FOOL_COUNT += 1
                                if 2 <= PC_FOOL_COUNT % 10 <= 4 and PC_FOOL_COUNT // 10 % 2 == 0:
                                    game.pc_hand_name.update(f'Колода Pc, дурак {PC_FOOL_COUNT} раза.')
                                else:
                                    game.pc_hand_name.update(f'Колода Pc, дурак {PC_FOOL_COUNT} раз.')

                            game.make_new_game_button.update('')
                            game.new_game()

        screen.fill(pygame.Color('black'))
        background_sprites.draw(screen)
        card_sprites.draw(screen)
        interface_sprites.draw(screen)
        bito_sprites.draw(screen)
        button_sprites.draw(screen)
        pygame.display.flip()
    terminate()

    # Баг - после бито ход не переходит на другого игрока. - пофиксил. - готово.
    # Баг - когда убирается козырь когда игрок берёт
    # - следующий ход не продолжается за Pc, а переходит на игрока, хотя дожен дальше идти на Pc. - пофиксил. - готово.
    #     Реализовать зону для карт. - готово.
    #     Реализовать интерфейс. - готово.
    #     Реализовать выкладку карт и сдвиг карт при добавлении новых. - готово.
    #     Реализовать набор карт со стола. Разбивку словаря с картами на их список,
    #     добор этих карт в руку игрока или пк, дорисовку их потом. - готово.
    #     Реализовать экземпляр класса карт/интерфейсов - бито,
    #     которое является одной картой с цифрой,- количеством карт, оставшихся в колоде. - готово.
    #     В случае отсутствия таких, кроме козыря - убирать. Плюс учесть то, что козырь тоже часть бито. - готово.
    #     Не учёл правило, что после первого хода - атаки, можно подкладывать только карты, которые уже были в игре,
    #     но могу его реализовать, когда завершу полностью игровой цикл и интерфейс. - готово.
    #     Доделать индикатор хода и его апдтейт - доделал. - готово.
    #     А также обновление статусов рубашек карт. - готово.
    #     Реализовать функцию добора. - готово.
    #     Реализовать ветвление в нажатие на кнопку брать, если нет возможных для хода карт,
    #     и проверку на то, что игрок может сходить. - готово.
    #     Баг: Карта, которой сходил компьютер всё еще числится в колоде. - вроде убрал, - готово
    #     Баг: Индикатор хода не работает и не обновляет значение. - индикатор хода убран. - готово.
    #     Баг: Туда же и баг со спрайтами, которые не обновляются. - исправлено. - готово.
    #     Баг спрайтов - остаются старые после реинициализации хода. - исправлено. - готово.
    #     Баг по ресурсам изображений: 9 буби = 9 черви. - перерисовал и закинул в дату. - исправил. - готово.
    #     Проблема: Карта, которую убрали из колоды методом поп - нужна при определении последнего юзера хода.
    #     Решение: Переопределить метод определения последнего юзера хода так,
    #     чтобы последняя карта там не учавствовала. - решено. - готово.
    #     Проблема в методе сравнения - решена. - готово.
    #     Баг: Последнее значение для хода меняется на первое для следующего -> не создается новая запись в словаре,
    #     а меняется последняя - Исправлен. - готово.
    #     Должна быть проверка чтобы не хватать карты другого игрока - готово.
    #     Реализовать перетаскивание - Не нужно. Сделал через тапы. - готово.
    #     Реализовать стейты атаки и защиты - готово.
    #     Реализовать ход/ выбор карты компьютером, метод выкладки карты для защиты, атаки. - готово.
    #     Проблема выдает что self.hodit это строка - готово.
    #     Def check_first_hod(self, *hands): - закинуть в класс игры - готово.
    #     Реализовать методы сравнения колод - готово.
