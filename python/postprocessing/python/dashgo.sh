#!/bin/bash


#/cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run0_80em/HTCondor_run

for file in *.submit
#for file in /cms/ldap_home/seungjun/nano/MC_b_bbar_4l/run0_80em/HTCondor_run/*.submit
do
    PWD=$(pwd)
#echo ${PWD:46:-15}
    width=${PWD:46:-15}"_"${file:19:-7}
#echo $width
    condor_submit -append accounting_group="group_cms" -batch-name $width  $file
done











																			  
