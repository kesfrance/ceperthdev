var months=new Array("January","February","March","April","May","June","July","August","September","October","November","December");
var dow = new Array("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
twodigityear = 0;

function leap(Q) {
var c=parseInt(Q,10);
return !(c%4) && (!(c%400) || (c%100));
}

function monthdays(b,c) {
if(b==2) 
 return leap(c)?29:28;
if(b==4||b==6||b==9||b==11)
 return 30;
else return 31;
}

function findInSelect(c,C) {
 for(var d=0;d<C.length;d++)
  if(c==C.options[d].text)
    return d;
  return 0;
}

function incMonth(b,u) {
 return((b+11+u)%12)+1;
}

function incYear(b,c,u) {
// Find year incremented month is in
// b=month, c=year, u=increment
 return c+((b+11+u)-(b+11+u)%12)/12-1;
}

function twoDigits(val) {
	return ((val < 10) ? '0' : '') + val + '';
}

function docal(obj, yearsBefore, yearsAfter) {
	if (typeof(yearsBefore) =='undefined') yearsBefore = 1;
	if (typeof(yearsAfter) =='undefined') yearsAfter = 2;
	val = obj.value;
	fields = val.split("-");
	error = 1;
	twodigityear = 0;
	if (fields.length == 3)
		try {
			error = 0;
			b = parseInt(fields[1], 10);
			c = parseInt(fields[2], 10);
			if (c < 100)  {
				c += 2000;
				twodigityear = 1;
			}
		}
		catch (e) {error = 1}
 	var B=new Date();
	year = B.getFullYear();
	if (error || b==0 || c==0 || c < year) {
		b = B.getMonth()+1; c = year;
	}

	j=0;
 	g=2;
	f=3
	calWin = window.open("","Calendar","width="+(20+f*227)+",height=220,top=200,left=200,resizable=yes");
	calWin.focus();
	firstYear = c-1
	lastYear = c+1
	calResultObj = obj;
	CalCalc(b,c,c-yearsBefore,c+yearsAfter);
}

function CalCalc(b,c,t,s,h,p) {
// Create the calendar in the box
//  b=month, c=year, t=minyear, s=maxyear, h=A|D, p=name
 var r=0;
 p = "Calendar Popup";
 h = '';	// no longer used
 var e,d;
 var tod = new Date();
 tod_day = tod.getDate(); tod_month = tod.getMonth()+1; tod_year = tod.getFullYear();

 if (c < t) {c=t; b=1}
 if (c>s) {c=s; b=12}

 var a = "";
 calWin.document.open();
 a+="<html><head>\n";
 a+="<script type='text/javascript'>\n";
 //a+="window.onload=pickerReady();\n";
 a+="function pickerReady() {\n var did = document.getElementById('datepickertable');\n var w = did.offsetWidth;\n var h = did.offsetHeight;\n resizeTo(Math.round(1.04*w),Math.round(1.50*h));\n}\n";
 a+="</script>\n";

 a+='<style type="text/css">\n';
 a+='td {font-family: Verdana, Arial, Geneva; font-size: 12px} \n';
 a+='.submit {FONT-SIZE: 11px; FONT-FAMILY: Verdana, Arial, Geneva;}\n';
 a+='</style>\n';
 a+="<title>"+p+"</title>\n</head>\n<body onload='pickerReady();' bgcolor=ffffff link='#000000'>"+"<center></center>\n";
 a+="<table id='datepickertable' border=0 cellspacing=0 cellpadding=3>\n";
 a+="<tr valign=top>\n";
 for(e=j;e<=g;e++) {
  a+="<td colspan=7 align=center bgcolor=#3E91D5>"+"<b><font color=white>"+months[incMonth(b,e)-1]+" "+incYear(b,c,e)+"</font></b></td>";
  a+="<td></td>";
 }
 a+="</tr>\n";
 var M=new Array("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
 a+="<tr align=right>\n";
 for(e=j;e<=g;e++) { 
  for(d=1;d<=7;d++)
   a+="<td><font color='"+(((d+r)%7||6)==6?"#FF9900":"#295181")+"'><b>"+M[(d+r)%7]+"</b></font></td>\n";
  if(e<g) 
   a+="<td></td>";
  }
 a+="</tr>\n";
 var A=0,q,i,z;
 var o=0;var n,w;
 while (A<f && o<10) { 
  a+="<tr>";
  for(e=j; e<=g; e++) { 
   i=incMonth(b,e);
   q=incYear(b,c,e);
   z=new Date(i+"/01/"+q);
   n=(z.getDay()+13-r)%7;
   w=monthdays(i,q)+n;
   for(d=o*7+1;d<(o+1)*7+1;d++) { 
    if(d<=n||d>w) 
     a+="<td>&nbsp;</td>\n";
    else { 
     if(d==w)
      A++;
	  bgc = (((d+r)%7||6)==6) ? "bgcolor='#EBECF0'" : "";
	  if (d-n==tod_day && i==tod_month && q==tod_year) bgc = "bgcolor = '#A9C3E6'";
     a+="<td "+bgc+" align=right>&nbsp;<a href='JavaScript:self.close();opener.storeDate("+(d-n)+","+i+","+q+");'>"+(d-n)+"</a></td>\n";
    }
   }
   if(e<g)
    a+="<td></td>";
  }
  o++;
  a+="</tr>\n";
 }
 if(o<6)
  a+="<tr><td>&nbsp;</td></tr>\n";
 var L=incMonth(b,-1);
 var K=incMonth(b,+1);
 var J=incYear(b,c,1);
 var I=incYear(b,c,-1);
 var H=incYear(b,c,g+1);
 var G=incYear(b,c,j-1);
 a+="<form action='javascript:return;'>\n<tr>\n"
  a+= "<td align=left colspan=11 bgcolor=#3E91D5>";

 // "previous month" button
 if(G<t)
  a+="&nbsp;";
 else 
  a+="<input type='button' class='submit' value=' < "+((f==1)?"":months[incMonth(b,j-1)-1]+" ")+"'"+"onClick='document.clear();opener.CalCalc("+L+","+I+","+t+","+s+",\""+h+"\",\""+p+"\")'>";
 if (J>t && K>2) a += printf("&nbsp;&nbsp;<input type='button' class='submit' value='<<%s' onClick='document.clear();opener.CalCalc(%s,%s,%s,%s,\"%s\",\"%s\")'>", [J-1,b,J-1,t,s,h,p]);

 a+="</td>"+"<td align=right colspan=12 bgcolor=#3E91D5>";
 if (J<s) a += printf("<input type='button' class='submit' value='>>%s' onClick='document.clear();opener.CalCalc(%s,%s,%s,%s,\"%s\",\"%s\")'>&nbsp;&nbsp;", [J+1,b,J+1,t,s,h,p]);

 // "next month" button
 if (H>s)
  a+="&nbsp;";
 else 
  a+="<input type='button' class='submit' value='"+((f==1)?"":months[incMonth(b,g+1)-1])+" > '"+"onClick='document.clear();opener.CalCalc("+K+","+J+","+t+","+s+",\""+h+"\",\""+p+"\")'>";
 a+="</td></tr>\n"
 a += "</form>";
 a+="</table>\n</body>\n</html>";
 calWin.document.write(a);calWin.document.close();
}

function storeDate(d, m, y) {
	// store date from popup selection
	if (twodigityear && y >= 2000) y -= 2000;
	calResultObj.value = twoDigits(d)+"-"+twoDigits(m)+"-"+y;
	if ($) $(calResultObj).change();
	
//	var evt = document.createEvent("HTMLEvents");
//	evt.initEvent("change", true, true );
//	calResultObj.dispatchEvent(evt);
	
	return;
}

function printf(fmt, vals) {
	var out = "";
	var strs = fmt.split("%s");
	if (strs.length != vals.length+1) alert("printf error "+fmt+" args="+vals.length+" "+vals[0]+" "+vals[1]);

	for(var i=0; i<vals.length; i++)
		out	+= strs[i] + vals[i];
	return out + strs[strs.length-1];
}


