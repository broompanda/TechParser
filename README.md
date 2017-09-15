# TechParser


<h3>Installation:</h3> 
<ol>
<li>Copy zip file to folder where you want to keep the tool.</li> 
<li>Unzip the folder.</li> 
<li>Open terminal and navigate to the folder created in step 2. </li>
<li>Execute the installation script: <b>./install_script.sh</b></li>
<li>Open a new terminal and confirm the alias are created in the bash_profile file : <b>cat ~/.bash_profile</b></li>
</ol>
<h4>Sample file</h4>

<pre width="30">alias gt='python /Users/christie/Documents/PycharmProjects/untitled/FileChar.py'<br>
alias pt=put_file<br>
put_file(){<br>
	&nbsp;file_number=$1<br>
	&nbsp;short_file_name=$2<br>
	&nbsp;if [ ! -z "$short_file_name" ]; then<br>
		&nbsp;&nbsp;directory=$(pwd)<br>
		&nbsp;&nbsp;full_file_name="$directory/$short_file_name"<br>
	&nbsp;fi<br>
	&nbsp;python /Users/christie/Documents/PycharmProjects/untitled/TrackFile2.py $file_number $full_file_name<br>
}<br></pre>



<h3>Using the tool:</h3>
<ul>
<li>Through your terminal, navigate to the folder where the show-tech is saved.</li>
<li>Assign it a number using the 'pt' command.</li>

<font size: 75%>You can keep track of multiple show-techs simultaneously: </font>
<ul><li>If you want to assign it as sh-tech number 1: <b>pt 1 show_tech_1_name.</b></li>
<li>If you want to assign it as sh-tech number 2: <b>pt 2 show_tech_2_name.</b></li>
</ul>

<li>Read from show-tech:</li>
Usage: gt [flags] file_number search_string
<ul>
<li>Reading from show-tech1: <b>gt 1 sh run</li></b>
<li>Reading from show-tech2: <b>gt 2 sh clock</li></b>
</ul>
</ul>
