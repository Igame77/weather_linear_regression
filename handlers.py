from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData
import config
from parser import Search
from LinearRegression import LinearRegression
from datetime import datetime

router = Router()

button_1 = KeyboardButton(text ='Москва')
button_2 = KeyboardButton(text = 'Санкт-Петербург')
button_3 = KeyboardButton(text = 'Краснодар')
button_4 = KeyboardButton(text = 'Саратов')
button_5 = KeyboardButton(text = 'Иваново')

class CityKeyBoard(CallbackData, prefix = 'any'):
    city: str
    year: int

class MonthKeyBoardData(CityKeyBoard, prefix = 'any'):
    month: str

class LinearRegData(CallbackData, prefix = 'any'):
    k: float
    m: float
    num: int

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_1, button_2],
        [button_3, button_4],
        [button_5]
    ]
)

@router.message(Command(commands=['start']))
async def process_start_command(message : Message):

    await message.answer(text = config.text_start, reply_markup= start_keyboard)

    
@router.message()
async def process_answer_command(message : Message):
    global msg
    buttons = []
    if message.text in ['Москва', 'Санкт-Петербург', 'Краснодар', 'Саратов', 'Иваново']:
        buttons = [[InlineKeyboardButton(text=f'20{j}{i}', callback_data= CityKeyBoard(city = message.text, year = int(f'20{j}{i}')).pack()) for i in range(9)] for j in range(3)]
        del(buttons[-1][-1])
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard= buttons)
        msg = await message.answer(text = 'Укажите год:', reply_markup= inline_keyboard)

@router.callback_query(CityKeyBoard.filter())
async def process_month_command(callback : CallbackQuery, callback_data: CityKeyBoard):
    global msg

    months = [['january','february','march','april'],['may','june','july','august'],['september','october','november','december']]
    buttons = [[InlineKeyboardButton(text = months[i][j],  callback_data= MonthKeyBoardData(city = callback_data.city, month = months[i][j], year = callback_data.year).pack()) for i in range(3)] for j in range(4)]
    
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)

    await msg.delete()
    msg = await callback.message.answer(text = 'Укажите месяц:', reply_markup = inline_keyboard)

@router.callback_query(MonthKeyBoardData.filter())
async def process_date_command(callback : CallbackQuery, callback_data : MonthKeyBoardData):
    global msg 
    city_dict = {'Москва' : 'moskva', 'Санкт-Петербург': 'sankt_peterburg', 'Краснодар' : 'krasnodar', 'Саратов' : 'saratov', 'Иваново' : 'ivanovo'}
    data = Search(city_dict[callback_data.city], callback_data.month, callback_data.year)
    model = LinearRegression()
    if data is not None:
        model.learn([i for i in range(len(data))], data)
        if len(data) >= 28:
            buttons = [[InlineKeyboardButton(text =str(i + j), callback_data = LinearRegData(k = model.k, m = model.m, num = (i + j)).pack()) for i in range(1,7) if (i + j) <= len(data)] for j in range(0,34, 7)]
        else:
            buttons = [[InlineKeyboardButton(text =str(i + j), callback_data = LinearRegData(k = model.k, m = model.m, num = (i + j)).pack()) for i in range(1,7) if (i + j) <= 31] for j in range(0,34, 7)]
        
    else:
        if callback_data.year >= datetime.now().year:
            data = [
                Search(city_dict[callback_data.city], callback_data.month, datetime.now().year - 1),
                Search(city_dict[callback_data.city], callback_data.month, datetime.now().year - 2)
                ]
            
        elif callback_data.year < 2009:
            data = [
                Search(city_dict[callback_data.city], callback_data.month, 2009),
                Search(city_dict[callback_data.city], callback_data.month, 2010)
                ]
        
        model.learn([i for i in range(len(data[0]))], data[0])
        k = model.k
        m = model.m
        model.clear_data()

        model.learn([i for i in range(len(data[1]))], data[1])

        k = (2 * k + model.k) / 3
        m = (2 * m + model.m) / 3
        buttons = [[InlineKeyboardButton(text =str(i + j), callback_data = LinearRegData(k = model.k, m = model.m, num = (i + j)).pack()) for i in range(1,7) if (i + j) <= 31] for j in range(0,34, 7)]
    
    buttons = [el for el in buttons if el != []]

    
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
    await msg.delete()
    msg = await callback.message.answer(text = 'Укажите дату:', reply_markup = inline_keyboard)


@router.callback_query(LinearRegData.filter())
async def process_predict_command(callback : CallbackQuery, callback_data : LinearRegData):
    global msg

    k = callback_data.k
    m = callback_data.m
    x = callback_data.num - 1

    result = str(round(k * x + m)) + '°'
    if '-' not in result: result = '+' + result

    await callback.message.answer(text= 'Результат: ' + result)


    


