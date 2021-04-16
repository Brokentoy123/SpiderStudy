from lxml import html as ht
# from lxml import
text = '''
<div>
   <ul>
       <li class="item-0"><a href="linke1.html">first item</a></li>
       <li class="item-1"><a href="linke2.html">second item</a></li>
       <li class="item-inactive"><a href="link3.html">third item</a></li>
       <li class="item-1"><a href="link3.html">forth item</a></li>
       <li class="item-0"><a href='link5.html'>fifth item</a></li>
   </ul>
</div>

'''
html = ht.etree.HTML(text)
result = ht.etree.tostring(html)
# print(result.decode('utf-8'))

html = ht.etree.parse('./templateHTML.html', ht.etree.HTMLParser())
result = ht.etree.tostring(html)
# print(result)

result = html.xpath('//li/a')
for item in result:
    print(ht.etree.tostring(item))
print(result)
