import asyncio
import aiosqlite

import aiosmtplib
from email.message import EmailMessage



async def send_mail(first_name, last_name, mail_to, index):
    message = EmailMessage()
    message["From"] = "user@gmail.com"
    message["To"] = mail_to
    message["Subject"] = "Рассылка"
    message.set_content(f"Уважаемый {first_name} {last_name}! Это тоестовое письмо")

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=465,
            use_tls=True,
            username="user@gmail.com",
            password="Password_user"
        )
        print(f"письмо номер {index} на адрес {mail_to} отправлено")
    except:
        await asyncio.sleep(5)
        print('Нет связи с почтовым сервером')


async def main():
    tasks = []
    index = 0
    async with aiosqlite.connect('contacts.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM contacts') as cursor:
            async for row in cursor:
                index = index + 1
                email_to = row['email'].split('_')
                email_to = ''.join(email_to)
                first_name = row['first_name']
                last_name = row['last_name']
                print(f'письмо номер {index} будет отправлено на {email_to}')
                task = asyncio.create_task(send_mail(first_name, last_name, email_to, index))
                tasks.append(task)

    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())

