cd %USERPROFILE%\Desktop
echo %cd%
:: go to installation folder \
cd lots-scraper\lots-scraper-installation
:: instal python\
echo %cd%
start python-installer.exe
:: go back to desktop \
cd %USERPROFILE%\Desktop
:: now install virtual env
pip install virtualenv
:: create a virtual env in desktop \
virtualenv venv
:: activate environment\
%USERPROFILE%\Desktop\venv\Scripts\activate
:: install libraries\
pip install pandas numpy lxml
pip install beautifulsoup4
pip install requests
pip install progressbar2 geopy
pip install selenium scipy termcolor
pip install dash
pip install dash_core_components dash_html_components
:: go back to installation folder \
cd %USERPROFILE%\Desktop\lots-scraper\lots-scraper-installation
:: install firefox \
start firefox-installation.exe
:: install git \
start git-installation.exe
:: clone the director in desktop \
cd %USERPROFILE%\Desktop
git clone https://github.com/zakariaelh/lots-scraper.git