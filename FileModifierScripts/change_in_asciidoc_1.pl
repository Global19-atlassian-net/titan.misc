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
#This script just changes the string
# C++ to {cpp} in files with extension .asciidoc
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

        if($filename =~ /(\.adoc)$/)
            {
            print("-> $filename\n");
            open(IN, $filename);
            $whole_file = <IN>;
            close(IN);

            # number of replacements
            $c = 0;
            
            $c += $whole_file =~ s!C\+\+!{cpp}!gs;
						$c += $whole_file =~ s!C\+\\\+!{cpp}!gs;
						$c += $whole_file =~ s!C\\?\+\\?\+!{cpp}!gs;
            if ( $c > 0 )
                {
                open(OUT, ">$filename");
                #utf8::encode($whole_file);
                print OUT $whole_file;
                close(OUT);
                print("License info changed: $filename\n");
                $total++;
                }
            }
        }
    }

load(".");
print("Total number of changed files: $total\n");
