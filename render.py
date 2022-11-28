import os
import webbrowser

class Renderer:
    def __init__(self,page,reachable,unreachable)-> None:
        self.pageName = page
        try:
            self.pageName = self.pageName.replace('/','').split(':')[1]
        except:
            pass
        self.reachAbleItems = reachable
        self.UnreachableItems = unreachable

    def RenderOutput(self)-> None:
        #Image list
        foundedImages = [x for x in self.reachAbleItems if x['type'] == 'image']
        unreachAbleImages = [x for x in self.UnreachableItems if x['type'] == 'image']

        #Javascript List
        foundedJs = [x for x in self.reachAbleItems if x['type'] == 'js']
        unreachAbleJs = [x for x in self.UnreachableItems if x['type'] == 'js']

        #Stylesheet List
        foundedstyle = [x for x in self.reachAbleItems if x['type'] == 'style']
        unreachAblestyle = [x for x in self.UnreachableItems if x['type'] == 'style']

        #Output html
        html = ''

        #Control the sample output file
        if os.path.exists('sample.html'):
            with(open('sample.html','r',encoding='utf-8')) as f:
                html = f.read()
        else:
            exit('Could not found sample output file')

        #Control output folder
        if os.path.exists('output'):
            with(open(f'output/{self.pageName}.html','w+',encoding='utf-8')) as f:
                #Replacement actions for output file
                html = html.replace('{{website}}',self.pageName)
                html = html.replace('{{totalImages}}',str(len(foundedImages)+len(unreachAbleImages)))
                html = html.replace('{{foundedImages}}',str(len(foundedImages)))
                html = html.replace('{{unreachAbleImages}}',str(len(unreachAbleImages)))
                html = html.replace('{{totalJs}}',str(len(foundedJs)+len(unreachAbleJs)))
                html = html.replace('{{foundedJs}}',str(len(foundedJs)))
                html = html.replace('{{unrechAbleJs}}',str(len(unreachAbleJs)))
                html = html.replace('{{totalStyles}}',str(len(foundedstyle)+len(unreachAblestyle)))
                html = html.replace('{{foundedStyles}}',str(len(foundedstyle)))
                html = html.replace('{{unreachAbleStyles}}',str(len(unreachAblestyle)))
                html = html.replace('{{foundedImagesTable}}',self.RenderTable(foundedImages))
                html = html.replace('{{unreachAbleImagesTable}}',self.RenderTable(unreachAbleImages))
                html = html.replace('{{foundedjsTable}}',self.RenderTable(foundedJs))
                html = html.replace('{{unreachAblejsTable}}',self.RenderTable(unreachAbleJs))
                html = html.replace('{{foundedStylesTable}}',self.RenderTable(foundedstyle))
                html = html.replace('{{unreachAbleStylesTable}}',self.RenderTable(unreachAblestyle))
                f.write(html)
            webbrowser.open(f'output/{self.pageName}.html')
        else:
            exit('Could not found output folder')
        

    def RenderTable(self,_list)-> str:
        html = '<table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">\n<tbody>'
        for item in _list:
            html += f'<tr>\n<td>{item["source"]}</td><td><a href="{item["source"]}" class="button is-link" target="_blank"><i class="fa-solid fa-eye"></i></a>\n</tr>\n'
                
        html+='</table>'
        return html
        
