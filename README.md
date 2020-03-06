## **Gamemuster**

Gamemuster is a python web application about games. It's build on django web-framework.

#### **Features**
App allows you to see information about games. All data comes form igdb.com.

App supports user registration. User can check others profile and add games to favorite.

#### **Requirements**
Python 3.8

#### **How to start an app**
1) Fill .env file with all required data, you can check all necessary variables in .env.template.
2) Run _docker build ._ and then _docker-compose up -d_ this will start redis, postgresql database, web application and celery.