# CoffeeRobot
## Компиляция на Linux:

Конфигурация с использованием toolchain

`cd build-arm`

`cmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain-arm.cmake`

`make`

## После успешной компиляции бинарник появится в:

`build-arm/bin/CoffeeRobot`

## Запуск на Raspberry Pi

После компиляции скопируйте бинарник на Raspberry Pi

На Raspberry Pi дайте права и запустите

`ssh user@192.168.1.101`

`chmod +x /home/user/CoffeeRobot`

`sudo /home/user/CoffeeRobot`

