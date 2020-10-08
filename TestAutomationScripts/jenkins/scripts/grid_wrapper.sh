#!/bin/bash

# Wrapper script for submitting jobs to the HUB Grid Endine

# --- FUNCTIONS ---

# Display usage
function Usage
{
    echo
    echo "grid_wrapper - Submit a job to the HUB Grid Engine"
    echo
    echo "Usage: grid_wrapper [OPTION]... COMMAND"
    echo
    echo "      COMMAND is submitted to the HUB Grid Engine for execution. The last parameter that does not mach with the patten of any option is treated as the COMMAND."
    echo
    echo "      Options:"
    echo
    echo "	-h , --help"
    echo "          Display this help."
    echo
    echo "      -r , --resources"
    echo "          Query the properties (architecture, OS type and version, number of processors) of all available executor nodes."
    echo
    echo "	-o , --output OUTFILE"
    echo "          The standard output of the job is saves in OUTFILE."
    echo
    echo "	-n , --no-merge"
    echo "           By default, the stderr stream is merged into stdout in the output file. This merge can be avoided by using this flag."
    echo
    echo "	-m , --mail MAILADDRESS"
    echo "          Send an e-mail to MAILADDRESS when the job ends."
    echo
    echo "	-q , --queue QUEUE_NAME"
    echo "          Submit the job to queue QUEUE_NAME"
    echo
    echo "	-A , --async"
    echo "          Run the job asynchronously (non-blocking). By default, the job is synchronous (blocking), therefore a subsequent command in the calling script is executed only when the job ended."
    echo
    echo "	-b , --binary"
    echo "          Treat COMMAND as binary, instead of script."
    echo
    echo "	-a , --arch ARCHITECTURE"
    echo "          Required architecture to run the job is ARCHITECTURE."
    echo
    echo "	-t , --ostype OSTYPE"
    echo "          Required OS type to run the job is OSTYPE."
    echo
    echo "	-v , --osver OSVERSION"
    echo "          Required OS version to run the job is OSVERSION."
    echo
    echo "	-p , --proc-num PROCNUM"
    echo "          Required number of processors to run the job is PROCNUM."
    echo

# command: last param not matching any of the options (- / --)

} # end of Usage

# Query and print available resources
function Resources
{
    echo "Querying available resources... (it may take a minute)"
    qconf -sel | while read LINE
    do
          OUTPUT=`qconf -se $LINE          | grep -E -o arch=[-.a-z0-9]+`
          OUTPUT="$OUTPUT `qconf -se $LINE | grep -E -o ostype=[-.a-z0-9]+`"
          OUTPUT="$OUTPUT `qconf -se $LINE | grep -E -o osver=[-.a-z0-9]+`"
          OUTPUT="$OUTPUT `qconf -se $LINE | grep -E -o num_proc=[0-9]+`"
          echo $OUTPUT
    done | sort | uniq --count
} # end of Resources


# --- MAIN ---

# Default parameters
OUTPUT="$HOME/output";
MERGE="y";
MAIL="n";
MAILADDR="";
QUEUE="sim";
SYNC="y";
ARCH="";
OSTYPE="";
OSVER="";
NUMPROC="";
BINARY="n";
CMD="";

# Add gridengine module
eval `/app/modules/0/bin/modulecmd sh add gridengine`

# Process parameters
while [ "$1" != "" ]; do
    case $1 in
	-h | --help )		Usage
                                exit
                                ;;
        -r | --resources )      Resources
                                exit
                                ;;
	-o | --output )		shift
				OUTPUT=$1
				;;
	-n | --no-merge )	MERGE="n"
				;;
	-m | --mail )		MAIL="e"
				shift
				MAILADDR=$1
				;;
	-q | --queue )		shift
				QUEUE=$1
				;;
	-A | --async )		SYNC="n"
				;;
	-b | --binary )		BINARY="y"
				;;
	-a | --arch )		shift
				ARCH=$1
				;;
	-t | --ostype )		shift
				OSTYPE=$1
				;;
	-v | --osver )		shift
				OSVER=$1
				;;
	-p | --proc-num )	shift
				NUMPROC=$1
				;;
	-* | --* )		echo Error: Invalid option $1
				Usage
				exit 1
				;;
        * )                     CMD=$1
                                ;;
    esac
    shift
done

# Exit if there is no command specified
if [ "$CMD" = "" ]; then
    echo "Error: command is missing"
    Usage
    exit 1
fi

# Display parameters
echo "Preparing to submit job to Grid Engine with the following parameters:"
echo "	Command:				$CMD"
echo "	Output file:				$OUTPUT"
echo "	Merge stderr into stdout:		$MERGE"
echo "	Queue name:				$QUEUE"
echo "	Synchronous execution (blocking):	$SYNC"
echo "	Command is binary (not script):		$BINARY"
echo "	Required architecture:			$ARCH"
echo "	Required OS type:			$OSTYPE"
echo "	Required OS version:			$OSVER"
echo "	Required number of processors:		$NUMPROC"
echo "	Send e-mail when job ends:		$MAIL"
echo "	Send e-mail to:				$MAILADDR"

# Store option tags (e.g. -M) with optional values
# reason: if unspecified, they should not appear in the option list of qsub
if [ "$MAIL" = "e" ]; then
    MAILADDR="-M $MAILADDR"
fi
if [ "$ARCH" != "" ]; then
    ARCH="-l arch=$ARCH"
fi
if [ "$OSTYPE" != "" ]; then
    OSTYPE="-l ostype=$OSTYPE"
fi
if [ "$OSVER" != "" ]; then
    OSVER="-l osver=$OSVER"
fi
if [ "$NUMPROC" != "" ]; then
    NUMPROC="-l num_proc=$NUMPROC"
fi

# Submit job
echo "$(date): Submitting job"
qsub  -q $QUEUE -sync $SYNC -o $OUTPUT -j $MERGE -b $BINARY -m $MAIL $MAILADDR $ARCH $OSTYPE $OSVER $NUMPROC  "$CMD"
OUT=$?
# Display end date and time
# note: if the job started asynchronously, it is not the job end time
echo "$(date): End of wrapper script"
exit $OUT