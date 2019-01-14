{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf200
{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red27\green31\blue34;\red244\green246\blue249;}
{\*\expandedcolortbl;;\cssrgb\c14118\c16078\c18039;\cssrgb\c96471\c97255\c98039;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #get to desktop\
cd %USERPROFILE%\\Desktop\
#go to installation folder \
cd lots-scraper-installation\
#instal python\
start python-installer.exe\
#go back to desktop \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 cd %USERPROFILE%\\Desktop\
#now install virtual env \
pip install virtualenv \
#create a virtual env in desktop \
virtualenv venv\
#activate environment\
venv/Scripts/activate\
#install libraries\
pip install pandas numpy lxml\
pip install beautifulsoup4\
pip install requests\
pip install progressbar2 geopy\
pip install selenium scipy termcolor\
pip install dash\
pip install dash_core_components dash_html_components\
#go back to installation folder \
cd lots-scraper-installation\
#install firefox \
start firefox-installation.exe\
#install git \
start git-installation.exe\
#clone the director in desktop \
cd %USERPROFILE%\\Desktop\
git clone https://github.com/zakariaelh/lots-scraper.git
\f1\fs27\fsmilli13600 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 \
}