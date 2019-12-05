#!/usr/bin/python3
import re
import subprocess


stats=subprocess.getoutput('gnunet-statistics').split('\n')

# for testing / running on machine that doesnt have gnunet-statistics.
# still makes cool tabulated tables, just from example data.
# generate file on your gnunet machine by 'gnunet-statistics > exampledata.txt' 
#f=open('exampledata.txt','r')
#stats=f.readlines()
#f.close()

page_head="""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>GNUNet Statistics</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<style>
	.bs-example{
    	margin: 20px;
    }
</style>
</head>
<body>
<div class="bs-example">
    <ul class="nav nav-tabs">"""

page_foot = """</ul>
</div>
</body>
</html>  """


final_page=""
final_page+=page_head

tab_content="""<div class="tab-content">
     <div class="tab-pane fade show active" id="home">
     stuff in home div?
     </div>"""

lines,j=[],[]
c=0
for i in stats:
    process = re.findall(' +([a-zA-Z]+) +(\#.+\:) +(\d+)',i)
    try:
        lines.append(list(process[0]))
    except:
        continue

categories = list(set([i[0] for i in lines]))
selection = -1
#build a table for each stat category
for i in categories:
    results,html_out = [],""
    selection+=1
    html_out+="""<li class="nav-item">
                <a href="#%s" class="nav-link" data-toggle="tab">%s</a>""" %(i,i)
    tab_content+="""<div class="tab-pane fade" id="%s">
                    <table id="datatable" class="table"><tbody><tr>"""  %(i)
    for i in lines:
        if i[0] == categories[int(selection)]:
            i[1] = " ".join(i[1].split()[1::]) # remove the leading hash.
            results.append(i[1::])
    results.sort()
    for i in results:
            tab_content+="<th>%s</th><th>%s</th></tr>" %(i[0],i[1])
            #print('{:<50}{:<}'.format(i[0],i[1])) #print a nice column for easy listenin'
    html_out+="</li>"
    tab_content+="</tbody></table></div>"
    final_page+=html_out

final_page+="</ul>"
final_page+=tab_content
final_page+=page_foot

f=open('web_stats.html', 'w')
f.write(final_page)
f.close()
