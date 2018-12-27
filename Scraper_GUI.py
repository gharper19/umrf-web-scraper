'''
## GUI - wxPython: 
- Frame Events: close, menu open/close, menu highlighted 

'''
import wx

class Scraper_Panel(wx.Panel):
    def __init__(self, parent):
        super(Scraper_Panel, self).__init__(parent)
        
        gridsizer= wx.GridSizer(rows=4, cols=2, vgap=0.1, hgap=0.5)
# For testing - fills out the grid with buttons
        for i in range(1, 8):
            btn= "Btn #" + str(i)
            gridsizer.Add(wx.Button(self, label=btn), 0, wx.EXPAND)

            self.SetSizer(gridsizer)


## Left off here prepping gridsizer to create config form 
    #  - Intro/Wiki for wx - https://wiki.wxpython.org/Getting%20Started
    #  - Function List - https://docs.wxpython.org/wx.functions.html
    #  - GridSizer - using https://www.bing.com/videos/search?q=gridsizer+wxpython&&view=detail&mid=FB917F6E21CDAC130F6FFB917F6E21CDAC130F6F&&FORM=VRDGAR
        #  - https://www.bing.com/videos/search?q=wx+python+introduction&qs=n&form=QBVR&sp=-1&pq=wx+python+introduction&sc=0-22&sk=&cvid=75A38F81643B4C8ABA8F9D65879948FE

# TODO: add text boxes for inputs, wrap in pyinstaller(installed)
    # Later: replace class and function comments, # , w/ '''str'''
class Scraper_Frame(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Scraper_Frame, self).__init__(*args, **kw)

        panel = Scraper_Panel(self)
        panel1= Scraper_Panel(self)

        gridsizer= wx.GridSizer(rows=4, cols=2, vgap=0.1, hgap=0.5)
    
        
        # create a panel in the frame - holds textboxes, buttons
        # panel2= Scraper_Panel(self)
        # start_button = wx.Button(panel, label="Start Scraping", pos=(75,90))

        # and put some text with a larger bold font on it
        # st = wx.StaticText(pnl, label="This is a Body Heading", pos=(25,25))
        # font = st.GetFont()
        # font.PointSize += 10
        # font = font.Bold()
        # st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar 
        self.CreateStatusBar()
        # self.SetStatusText("")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = Scraper_Frame(None, title='EPDSM KPI Scraper')
    frm.Show()
    app.MainLoop()
