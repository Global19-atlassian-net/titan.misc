#!/usr/bin/perl

#use utf8;

#### This script synchronize gerrithub to github ####
# Cd into the root directory containing all Github directory and run this script
# This script 
# 1. goes into each github repository, then
# 2. Modifies the local .git/config file via command "git config"
# 2.a The git.remote.origin is set for the gerritdir, e.g 
#     git config remote.origin.url "ssh://balaskoa@review.gerrithub.io:29418/eclipse/titan.ProtocolModules.COMMON.git"
# 2.b The git.remote.github.url is set for the github address e.g 
#     git config git.remote.github.url "git@github.com:eclipse/titan.ProtocolModules.COMMON.git"
# 3. Pulls there the content from the github repo
# 4. pushes the content to the gerrit repository of the same project
#
#Prerequisites:
# 1.Git repositories exists (remote origin is not necessarily good); 
# 2.perl 5.x is available
# 
# to read the whole file at once, not just line-by-line
# http://www.kichwa.com/quik_ref/spec_variables.html
undef $/;

use warnings;
#use strict;
use Cwd 'abs_path';
use File::Basename;

#print abs_path($0);

local $fileindex = 0;
#total number of changed files
local $total_found = 0; #git.eclipse.org found int the repo's config file, i.e sync is not necessary
local $total_not_found = 0; #git.eclipse.org not found int the repo's config file, i.e sync necessary

local $gitconfig_cmd_gerrit_first_part = 'git config remote.origin.url "ssh://balaskoa@review.gerrithub.io:29418/eclipse/';
local $gitconfig_cmd_github_first_part = 'git config remote.github.url "git@github.com:eclipse/';

### If the arg is a git repository, executes a git commit and a git push command in the repo.
### If the arg is not a repository but a folder, it calls itself resursively for all dir element
### For files it doesn't do anything
sub load {
    my $filename = shift; # 1st parameter
    my $f = "F".$fileindex++;
	#print("$filename dir open is starting\n");
	if( -e $filename and -d $filename ) {
		#print ("*************************************\n");
		#print("$filename is a directory!!!\n");
        # $filename is a directory
		my $gitdir = $filename."/\.git"; # for Unix
		if( -e $gitdir and -d $gitdir)
			{
			#filename is a git repository
		
			#if the config file contains 'git.eclipse.org' then do not process this repo - eclipse.org is not requires sync (?)
			my $cfgfile = $gitdir."/config";
			#print ( $cfgfile."\n" );
			if ( -e $cfgfile ) {
				open(FH, $cfgfile) or ( print("File $cfgfile not found") and return); 
				my $String = <FH>;
				close(FH);
				if( $String =~ m!git\.eclipse\.org! ) { 
					#print ( $String );
					print (">>>>>git.eclipse.org string found.\n");
					$total_found++;
					return;
				}
			} else {
				print ( ">>>>Error in repo ", $gitdir,  " . config file is not found" );
				return;
			}
			
			my $reponame = basename($filename); #last segment of the path
			print ( ">>>>>git\.eclipse\.org string not found in repo ", $reponame," .Synchronization starts\n" );
			$total_not_found++;
			
			#set remote.origin to gerrit
			my $gerrit_url_cmd = "$gitconfig_cmd_gerrit_first_part"."$reponame".'.git"';
			#print("Repo name: $reponame \n");
			print("$gerrit_url_cmd","\n");
			chdir "$filename";
			my $retval;
			$retval = `$gerrit_url_cmd`;
			
			##set gerrit fetch:
			print ('git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"',"\n");
			$retval = `git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"`;
			
			##set remote.github to github:
			my $github_url_cmd =  $gitconfig_cmd_github_first_part.$reponame.'.git"';
			print ( "$github_url_cmd", "\n" );
			$retval = `$github_url_cmd`;
			print ('git config remote.github.fetch "+refs/heads/*:refs/remotes/github/*"',"\n");
			# $retval = `git config remote.github.fetch "+refs/heads/*:refs/remotes/github/*"`;
			
			print ('git config branch.master.remote "origin"',"\n");
			$retval = `git config branch.master.remote "origin"`;
			 
			print ("git pull github master\n");
			$retval = `git pull github master`;
			# print "Git pull from github result 3:\n$retval\n";
			print ("git push origin master\n");
			$retval = `git push origin master`;
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
					print ("*************************************\n");
					print("$longfilename \n");
					load($longfilename);
					}
				}
				closedir($f);
				#print("dir closed\n");
				
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

#### MAIN ####
print ("*************************************************************\n");
print ("Sychronization github->gerrit started\n");
print ("*************************************************************\n\n");
local $originaldir = abs_path("."); #`pwd`;
print ("$originaldir\n");
load("$originaldir");
print ("*************************************************************\n");
print("Total number of synchronized repo     : $total_not_found\n");
print("Total number of not synchronized repo : $total_found\n");
print ("*************************************************************\n");
