#!/usr/bin/perl
###############################################################################
# Copyright (c) 2000-2021 Ericsson Telecom AB
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
#This script just commits and pushes all git repository 
#Cd into the root directory and run
#In each subdirs which is git repository will be executed a git commit and a git push.
#Prerequisites:
# 1.Git repositories has good config;
# 2.perl 5.x is available
# 
# to read the whole file at once, not just line-by-line
# http://www.kichwa.com/quik_ref/spec_variables.html
undef $/;

use warnings;
#use strict;
use Cwd 'abs_path';
#use File::Basename;

#print abs_path($0);

local $fileindex = 0;
#total number of changed files
local $total = 0;

### If the arg is a git repository, executes a git commit and a git push command in the repo.
### If the arg is not a repository but a folder, it calls itself resursively for all dir element
### For files it doesn't do anything
sub load
    {
    my $filename = shift; # 1st parameter
    my $f = "F".$fileindex++;
	print("$filename dir open is starting\n");
	print("$filename\n");
	
	if( -e $filename and -d $filename ) {
		print("$filename is a directory!!!\n");
        # $filename is a directory
		my $gitdir = $filename."/\.git"; # for Unix
		if( -e $gitdir and -d $gitdir)
			{
			#filename is a git repository
			print("===$filename is a git repo===\n");
			print("$gitdir found!\n");
			#my $msg = `pwd`;
			#print("$msg\n");
			chdir "$filename";
			my $d = `pwd`;
			print "$d\n";
			my $retval;
			$retval = `git status`;
			print "Git status result:\n$retval\n";
			
			#commit:
			$retval = `git commit -sam "Copyright date changed for 2000-2020"`;
			print "Git commit result:\n$retval\n";
			
			#push
			$retval = `git push`;
			print "Git push result:\n$retval\n";
			$total++;
			#do not go inside this dir!
			
		} else 
		{
			if(opendir($f, $filename)) {
				print("$filename is not a git directory, go inside\n");
			
				#if it is not a git repository, go inside
				while(local $newfilename = readdir($f))
				{
					if(!($newfilename =~ /^\.(\.)?$/))  # filter . .. .git
					{
					my $longfilename = $filename."/".$newfilename; # for Unix
					#local $longfilename = $filename."\\".$newfilename; # for DOS/Windows
					print("$longfilename \n");
					load($longfilename);
					}
				}
				closedir($f);
				print("dir closed\n");
				
			} else {
				print("$filename folder opening error\n");
			}
		}

	}
    else 
	{
		print("$filename is a file. Not processed\n");
    }
    }#end of load

local $originaldir = abs_path("."); #`pwd`;
load("$originaldir");
print("\nTotal number of changed files: $total\n");
