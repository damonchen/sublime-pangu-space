# coding: utf-8

import re

import sublime
import sublime_plugin


# code from pangu (https://github.com/vinta/pangu.py)

"""
Paranoid text spacing for good readability, to automatically insert whitespace
between CJK (Chinese, Japanese, Korean) and half-width characters (alphabetical
letters, numerical digits and symbols).

>>> import pangu
>>> pangu.spacing_text('當你凝視著bug，bug也凝視著你')
'當你凝視著 bug，bug 也凝視著你'
>>> pangu.spacing_file('path/to/file.txt')
'與 PM 戰鬥的人，應當小心自己不要成為 PM'
"""

__version__ = '1.0.0'


def u(s):
    return s


CJK_QUOTE_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])(["\'])'
      ))
QUOTE_CJK_RE = re.compile(
    u(r'(["\'])([\u3040-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))
FIX_QUOTE_RE = re.compile(
    u(r'(["\'\(\[\{<\u201c]+)(\s*)(.+?)(\s*)(["\'\)\]\}>\u201d]+)'))
FIX_SINGLE_QUOTE_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])()(\')([A-Za-z])'
      ))

CJK_HASH_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])(#(\S+))'
      ))
HASH_CJK_RE = re.compile(
    u(r'((\S+)#)([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))

CJK_OPERATOR_ANS_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\+\-\*\/=&\\|<>])([A-Za-z0-9])'
      ))
ANS_OPERATOR_CJK_RE = re.compile(
    u(r'([A-Za-z0-9])([\+\-\*\/=&\\|<>])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))

CJK_BRACKET_CJK_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\(\[\{<\u201c]+(.*?)[\)\]\}>\u201d]+)([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))
CJK_BRACKET_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([\(\[\{<\u201c>])'
      ))
BRACKET_CJK_RE = re.compile(
    u(r'([\)\]\}>\u201d<])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))
FIX_BRACKET_RE = re.compile(
    u(r'([\(\[\{<\u201c]+)(\s*)(.+?)(\s*)([\)\]\}>\u201d]+)'))

FIX_SYMBOL_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([~!;:,\.\?\u2026])([A-Za-z0-9])'
      ))

CJK_ANS_RE = re.compile(
    u(r'([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])([A-Za-z0-9`\$%\^&\*\-=\+\\\|/@\u00a1-\u00ff\u2022\u2027\u2150-\u218f])'
      ))
ANS_CJK_RE = re.compile(
    u(r'([A-Za-z0-9`~\$%\^&\*\-=\+\\\|/!;:,\.\?\u00a1-\u00ff\u2022\u2026\u2027\u2150-\u218f])([\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff])'
      ))


def spacing_text(text):
    """
    Perform paranoid text spacing on text.
    """
    # always use unicode
    # if IS_PY2 and isinstance(text, str):
    #     text = text.decode('utf-8')

    if len(text) < 2:
        return text

    text = CJK_QUOTE_RE.sub(r'\1 \2', text)
    text = QUOTE_CJK_RE.sub(r'\1 \2', text)
    text = FIX_QUOTE_RE.sub(r'\1\3\5', text)
    text = FIX_SINGLE_QUOTE_RE.sub(r'\1\3\4', text)

    text = CJK_HASH_RE.sub(r'\1 \2', text)
    text = HASH_CJK_RE.sub(r'\1 \3', text)

    text = CJK_OPERATOR_ANS_RE.sub(r'\1 \2 \3', text)
    text = ANS_OPERATOR_CJK_RE.sub(r'\1 \2 \3', text)

    old_text, text = text, CJK_BRACKET_CJK_RE.sub(r'\1 \2 \4', text)
    if old_text == text:
        text = CJK_BRACKET_RE.sub(r'\1 \2', text)
        text = BRACKET_CJK_RE.sub(r'\1 \2', text)
    text = FIX_BRACKET_RE.sub(r'\1\3\5', text)

    text = FIX_SYMBOL_RE.sub(r'\1\2 \3', text)

    text = CJK_ANS_RE.sub(r'\1 \2', text)
    text = ANS_CJK_RE.sub(r'\1 \2', text)
    return text

    # return text.strip()


class PanguSpaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, user_input=None):
        regions = self.view.find_all(".*", sublime.IGNORECASE)

        for region in reversed(regions):
            text = self.view.substr(region)
            text = spacing_text(text)
            self.view.replace(edit, region, text)


class EnsureSpaceBetweenChineseAndEnglish(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        filename = view.file_name()
        if filename and filename.endswith('.md'):
            print(filename)
            view.run_command('pangu_space')
