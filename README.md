# lots-scraper

Webapp that crawls lots and the average house price around each lot

In order to install this, we have to follow the steps below. 

1. We need to have python3.6 installed in our computer. To install python 3, please follow the steps below: 
  1. go to this [link](https://www.python.org/downloads/windows/)
  2. Under `Python 3.6.8 - 2018-12-24`, select `Windows x86-64 executable installer`
  3. Download it
  4. Install it. When start installing, make sure to check **Add to PATH**. Then, choose all the default settings and click Next. 

2. Now, let's open the command line by going to the search bar in our desktop and write 'Command Prompt'. Launch Command Prompt.

3. We would like to install a virtual environment library. To do that, copy and paste the code below in your command line and press `Enter` 

```
pip isntall virtualenv
```
4. Create a virtual environment as follows and activate it.
```
virtualenv venv 
cd venv/Scripts/activate
```

5. Install libraries, copy line by line to make sure it all installs correctly
```
pip install pandas, numpy
pip install lxml 
pip install beautifulsoup4
pip install requests
pip install progressbar2, geopy
pip install selenium 
pip install scipy 
pip install termcolor
pip install dash
pip install dash_core_components, dash_html_components
```

Now, **close the directory**


6. Now, we would like to install the Firefox browser. Click on this [link](https://www.mozilla.org/en-US/firefox/new/) and Download Firefox. Then, install it. 

7. Now we would like to install the Git command line. We do this as follows. Go to [git](https://gitforwindows.org/), and click on Download and install it with the default options. 

8. Clone the app directory into our the Desktop of our local computer. Go to the searchbar of your computer and type `Git Bash`
```
cd Desktop
git clone https://github.com/zakariaelh/lots-scraper.git
```

9. Let's run a test to see if our environment is set correctly. Go back to the `Command Prompt`. Go to the search bar and type `Command Prompt. 
  - Enter the following lines: 
  ```
  cd Desktop
  cd venv/Scripts/activate 
  cd lots-scraper
  python test-scraper
  ```
  You might get a pop-up asking you to Allow permissions. Please do! 
  
10. Now, run the app 
```
python app6.py
```

