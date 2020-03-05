#!/usr/bin/perl
###############################################################################
# Copyright (c) 2000-2020 Ericsson Telecom AB
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.html
#
# Contributors:
#   Balasko, Jeno
#   Lovassy, Arpad
#
###############################################################################
#use utf8;
#This script just changes the year of the new copyright headers
# to read the whole file at once, not just line-by-line
# http://www.kichwa.com/quik_ref/spec_variables.html
undef $/;

$fileindex = 0;
#total number of changed files
$total = 0;

sub load
    {
    local $filename = shift; # 1st parameter
    local $f = "F".$fileindex++;
    if(opendir($f, $filename))
        {
        # $filename is a directory
        while(local $newfilename = readdir($f))
            {
            if(!($newfilename =~ /^\.(\.|git)?$/))  # filter . .. .git
                {
                local $longfilename = $filename."/".$newfilename; # for Unix
                #local $longfilename = $filename."\\".$newfilename; # for DOS/Windows

                load($longfilename);
                }
            }
        closedir($f);
        }
    else
        {
        # $filename is a file

        if($filename =~ /(README.*|adoc|ttcn3_help|titanver|Makefile.*|\.(properties|iml|g4|tpd|java|ttcn|cc|hh|xml|prj|py|xsd|sh|c|h|html|l|y|asn|1|xsl|fast_script|script|pl|cfg|txt|hhc|hhp|dot|ttcnpp|converter|ttcnin|ttcn3|dat|grp|prj|awk|ddf|pats|css|js|launch|rdf|lex|tpl)|Readme|ttcn3.*|compiler|make|license|script_not_running)$/)
            {
            #print("-> $filename\n");
            open(IN, $filename);
            $whole_file = <IN>;
            close(IN);

            # number of replacements
            $c = 0;
			# $c += $whole_file =~ s/Copyright \(c\) 20[0-1][0-9][ \,\-]*20[0-1][0-8][ \,]*Ericsson AB/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
			$c += $whole_file =~ s/Copyright \(c\) 20[0-1][0-9][ \,\-]*20[0-1][0-9][ \,]*Ericsson Telecom AB/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
			# $c += $whole_file =~ s/Copyright \(c\)[ ]*20[0-1][0-9][ ]*Ericsson AB/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;			
			#$c += $whole_file =~ s/Copyright Ericsson \(c\) Telecom AB 2000-201[0-9]/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
			# $c += $whole_file =~ s/Copyright Test Competence Center \(TCC\) ETH 20[0-1][0-9]/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
			# $c += $whole_file =~ s/Copyright 2012 Test Competence Center/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
            # $c += $whole_file =~ s/Copyright \(c\) 2000\-201[0-8]   Ericsson Telecom AB/Copyright \(c\) 2000\-2019 Ericsson Telecom AB/gs;
            # $c += $whole_file =~ s/Copyright \(c\) 2000\-201[0-7] Ericsson Telecom AB/Copyright (c) 2000\-2019 Ericsson Telecom AB/gs;
            $c += $whole_file =~ s/Copyright Ericsson Telecom AB 201[0-9]/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
			$c += $whole_file =~ s/Copyright Ericsson AB 201[0-9]/Copyright (c) 2000-2020 Ericsson Telecom AB/gs;
            $c += $whole_file =~ s/Copyright Ericsson Telecom AB 2000\-2014/Copyright \(c\) 2000\-2020 Ericsson Telecom AB/gs;
            if ( $c > 0 )
                {
                open(OUT, ">$filename");
                #utf8::encode($whole_file);
                print OUT $whole_file;
                close(OUT);
                print("Copyright info changed: $filename\n");
                $total++;
                }
            }
        }
    }

load(".");
print("Total number of changed files: $total\n");
