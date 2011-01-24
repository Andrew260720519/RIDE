# Copyright 2010 Orbitz WorldWide
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''runProfiles.py

This module contains profiles for running robot tests via the
runnerPlugin.

Each class that is a subclass as BaseProfile will appear in a
drop-down list within the plugin. The chosen profile will be used to
build up a command that will be passed in the tests to run as well as
any additional arguments.
'''

import wx
import os

class BaseProfile(object):
    '''Base class for all test runner profiles

    At a minimum each profile must set the name attribute, which is
    how the profile will appear in the dropdown list.
    
    This class (BaseProfile) will _not_ appear as one of the choices.
    Think of it as an abstract class, if Python 2.5 had such a thing.
    '''

    # this will be set to the plugin instance at runtime
    plugin = None

    def __init__(self, plugin):
        '''plugin is required so that the profiles can save their settings'''
        self.plugin = plugin
        self.toolbar = None

    def get_toolbar(self, parent):
        '''Returns a panel with toolbar controls to be shown for this profile'''
        if self.toolbar is None:
            self.toolbar = self.TagsPanel(parent)
        return self.toolbar

    def get_custom_args(self):
        '''Return a list of arguments unique to this profile'''
        args = []
        if self.plugin.apply_include_tags and self.plugin.include_tags:
            for include in self.plugin.include_tags.split(","):
                include = include.strip()
                if len(include) > 0:
                    args.append("--include=%s" % include)
        if self.plugin.apply_exclude_tags and self.plugin.exclude_tags:
            for exclude in self.plugin.exclude_tags.split(","):
                exclude = exclude.strip()
                if len(exclude) > 0:
                    args.append("--exclude=%s" % exclude)
        return args

    def get_command_prefix(self):
        '''Returns a command and any special arguments for this profile'''
        if os.name == "nt":
            return ["pybot.bat"]
        else:
            return ["pybot"]

    def TagsPanel(self, parent):
        '''Create a panel to input include/exclude tags'''
        panel = wx.Panel(parent, wx.ID_ANY)
        include_cb = self._create_checkbox(panel, self.plugin.apply_include_tags,
                                          "Only run tests with these tags")
        exclude_cb = self._create_checkbox(panel, self.plugin.apply_exclude_tags,
                                          "Skip tests with these tags")
        include_tags = wx.TextCtrl(panel, wx.ID_ANY, size=(150,-1),
                                       value=self.plugin.include_tags)
        exclude_tags = wx.TextCtrl(panel, wx.ID_ANY, size=(150,-1),
                                       value=self.plugin.exclude_tags)

        panel.Bind(wx.EVT_CHECKBOX, self.OnIncludeCheckbox, include_cb)
        panel.Bind(wx.EVT_CHECKBOX, self.OnExcludeCheckbox, exclude_cb)
        include_tags.Bind(wx.EVT_TEXT, self.OnIncludeTagsChanged)
        exclude_tags.Bind(wx.EVT_TEXT, self.OnExcludeTagsChanged)

        panelsizer = wx.GridBagSizer(2,2)
        panelsizer.Add(include_cb, (0,0), flag=wx.EXPAND)
        panelsizer.Add(exclude_cb, (0,1), flag=wx.EXPAND)
        panelsizer.Add(include_tags, (1,0), flag=wx.EXPAND)
        panelsizer.Add(exclude_tags, (1,1), flag=wx.EXPAND)
        panelsizer.AddGrowableCol(0)
        panelsizer.AddGrowableCol(1)
        panel.SetSizerAndFit(panelsizer)
        return panel

    def _create_checkbox(self, parent, value, title):
        checkbox = wx.CheckBox(parent, wx.ID_ANY, title)
        checkbox.SetValue(value)
        return checkbox

    def set_setting(self, name, value):
        '''Sets a plugin setting'''
        self.plugin.save_setting(name, value, delay=2)

    def OnExcludeCheckbox(self, evt):
        self.set_setting("apply_exclude_tags", evt.IsChecked())

    def OnIncludeCheckbox(self, evt):
        self.set_setting("apply_include_tags", evt.IsChecked())

    def OnIncludeTagsChanged(self, evt):
        self.set_setting("include_tags", self.includeTags.GetValue())

    def OnExcludeTagsChanged(self, evt):
        self.set_setting("exclude_tags", self.excludeTags.GetValue())


class PybotProfile(BaseProfile):
    '''A runner profile which uses pybot

    It is assumed that these programs are on the path
    '''
    name = "pybot"
    def get_command_prefix(self):
        if os.name == "nt":
            return ["pybot.bat"]
        else:
            return ["pybot"]
