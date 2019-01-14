# lots-scraper

Webapp that crawls lots and the average house price around each lot

## Easy Installation:

Download the installation folder, and put in your Desktop. 
1. Start by installing Python. To do so: right-click on `python-installer` and click on `Run as Administrator`. **Warning:** Check **Add Python 3.6 to PATH** on the first screen of installation. Then just keep clicking Next.
        - You might get a pop-up asking to allow permission to make changes, please press Yes. 
2. Install firefox. Likewise, right on `firefox-installation` and click on `Run as Administrator`.
3. Install git. Same as above. (Run as administrator)
4. Set-up the environment where we will run the app. Right click on `py-setup` and click on `Run as Administrator`. 
5. Now, go to your desktop and you will find a new directory called `lots-scraper`. 
6. Run first a test by double-cliking on `test-scraper`
7. To run the app, double-click on `app6`, then go to http://http://127.0.0.1:8050


## Long Installation
In order to install this, we have to follow the steps below. 

1. We need to have python3.6 installed in our computer. To install python 3, please follow the steps below: 
    - go to this [link](https://www.python.org/downloads/windows/)
    - Under `Python 3.6.8 - 2018-12-24`, select `Windows x86-64 executable installer`
    - Download it
    - Install it. When you open the installation window, make sure to check in the bottom of the window **Add Python 3.6 to PATH**. Then, click **Install Now** and continue by clicking Next. 

2. Now, let's open the command line by going to the search bar in our desktop and write 'Command Prompt'. Launch Command Prompt.

3. We would like to install a virtual environment library. To do that, copy and paste the code below in your command line and press `Enter` 

```
pip install virtualenv
```
4. Create a virtual environment in our Desktop as follows and activate it.
```
cd Desktop
virtualenv venv 
venv\Scripts\activate
```

5. Install libraries, copy line by line to make sure it all installs correctly
```
pip install pandas numpy
pip install lxml 
pip install beautifulsoup4
pip install requests
pip install progressbar2 geopy
pip install selenium 
pip install scipy 
pip install termcolor
pip install dash
pip install dash_core_components dash_html_components
```

Now, **close the command line window**


6. Now, we would like to install the Firefox browser. Click on this [link](https://www.mozilla.org/en-US/firefox/new/) and Download Firefox. Then, install it. 

7. Now we would like to install the Git command line. We do this as follows. Go to [git](https://gitforwindows.org/), and click on Download and install it with the default options (i.e. keep cliking Next until installation finishes). 

8. Clone the app directory into our the Desktop of our local computer. Go to the searchbar of your computer and type `Git Bash` then enter the following lines one by one. 
```
cd Desktop
git clone https://github.com/zakariaelh/lots-scraper.git
```

9. Let's run a test to see if our environment is set correctly. We need to go back to the `Command Prompt`. Go to the search bar and type `Command Prompt. 
  - Enter the following lines: 
  ```
  cd Desktop
  venv\Scripts\activate 
  cd lots-scraper
  python test-scraper.py
  ```
  - You might get a pop-up aking you to `Allow Access`, please click `Allow acess`. 
  You might get a pop-up asking you to Allow permissions. Please do! 
  
10. Now, let's run the app. Go back to the directory and enter.
```
python app6.py
```

