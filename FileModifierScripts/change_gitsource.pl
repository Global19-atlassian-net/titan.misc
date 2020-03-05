#!/usr/bin/perl

#use utf8;
#This script just changes the "url = http://git.eclipse.org/gitroot/titan" for "url = ssh://jbalasko\@git.eclipse.org:29418/titan/"
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
            if(!($newfilename =~ /^\.(\.)?$/))  # filter . .. .git
                {
                local $longfilename = $filename."/".$newfilename; # for Unix
                #local $longfilename = $filename."\\".$newfilename; # for DOS/Windows
				#print("$longfilename comes...");
                load($longfilename);
                }
            }
        closedir($f);
        }
    else
        {
        # $filename is a file

        if($filename =~ /(config)$/)
            {
            print("-> $filename\n");
            open(IN, $filename);
            $whole_file = <IN>;
            close(IN);

            # number of replacements
            $c = 0;
			$c += $whole_file =~ s!url = http://git.eclipse.org/gitroot/titan/!url = ssh://jbalasko\@git.eclipse.org:29418/titan/!gs;
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
