
########################################################
#Author: Olivia Choudhury
#Last modified: 06/09/2017
#version 6_8: keep ref_base for low-confidence correction + check value of J1 (not J2-J1) for confidence threshold
########################################################

import os, fileinput, re, sys
from collections import defaultdict
import numpy,operator

def median(lst):
    return numpy.median(numpy.array(lst))

# For iterative correction, create a new pileup file to store the lines with low-confidence correction
pileupiter=sys.argv[3]
f_pileupiter=open(pileupiter,'w')

# Quick Correction when >90% SRs vote for one allele
f_pileup=sys.argv[1]
l_pileup=open(f_pileup).readlines()
ref_file=sys.argv[2]

# Count the number of sequences in the fasta file
num_LRread=len(l_pileup) / 2

cutoff_quickcorrect=0.85
SR_readlength=sys.argv[5]
#num_LRread=sys.argv[4]
max_qualscore=60
#conf_threshold=0.005
conf_threshold=1.2


# create a dict from reference PB fasta file,
# where key=header and val=read
dict_ref={}
#ref_file='/afs/crc.nd.edu/group/NDBL/data/PB_ErrorCorrection/Fun_10files/File_4/4.fa'
fref=open(ref_file,'r')

c=0
while(c<=int(num_LRread)):
	# Check for header
	l1=fref.readline()
	l2=fref.readline()
	l1=l1.rstrip('\n')
	l2=l2.rstrip('\n')

	dict_ref[l1]=l2
	c+=1

# Create a list to append the header names
# easier to access by index
list_ref=[]

# Create a list to store pos so that the end pos of previous reference can be stored
list_pos=[]

# Create a dict where key=header and val=startpos_endpos of that header in pileup file
#dict_pilepos={}
dict_pilepos=defaultdict(list)

# create a dict where key=header and val=end_pos 
d_ref={}

#Use Subset_sortedpos.sam (output file of 'Create_SubsetSAM.sh') to get number of matches
#Create a dict where key=ref_header and val=list containing no. of matches based on the field 'MD:Z'
#Parse MD:Z field to fetch only digit
#f_subsetSAM='/afs/crc.nd.edu/group/NDBL/ochoudhu/PB_ErrorCorrection/Data_New/Ecoli_Simulated/bwa_mem_def/Correction/Subset_sortedpos.sam'
f_subsetSAM=sys.argv[4]
list_subsetSAM=open(f_subsetSAM).readlines()

d_SR_matchnorm=defaultdict(list)

#create dict where key=ref_header and val=MAPQ of each SR that aligns to the ref_header
d_SR_qual=defaultdict(list)

for line_SAM in list_subsetSAM:

	# Ignore header lines
	if (line_SAM[0]!="@"):

		line_SAM=line_SAM.rstrip('\n')
		col_SAM=line_SAM.split()

		ref_SAM=col_SAM[2]

		#Ignore lines that have '*' in Ref field 
		if (ref_SAM!='*'):

			# To alter MAPQ=0 to MAPQ=1
			MAPQ_SAM=int(col_SAM[4])+1

			#-----------------------------------
			#Added for version 5 - Normalize quality weight
			MAPQ_SAM=MAPQ_SAM/float(max_qualscore)
			#-----------------------------------

			# MD:Z flag does not have a fixed column (not always the last column)
			for field in col_SAM:
				if ('MD:Z' in field):
					MDZ_val=field.split('MD:Z:')[1]
					num_match=0
					# Parse to get only digits
					l_match=re.findall(r'[\d]+',MDZ_val)
					for i_match in l_match:
						num_match=num_match+int(i_match)
			# Normalize the number of matches
			matchnorm=num_match/float(SR_readlength)
			d_SR_matchnorm[ref_SAM].append(matchnorm)

			# Store MAPQ value of each aligned SR
			d_SR_qual[ref_SAM].append(MAPQ_SAM)


#create dict where key=ref_header and val=list containing position on ref where each SR begins alignment
d_SR_startpos=defaultdict(list)

# create dict where key=ref_header and val=list containing position on ref where each SR ends alignment
d_SR_endpos=defaultdict(list)

# Create data structures to save information about the SRs aligning to each ref_header
for line_p in l_pileup:

	line_p=line_p.rstrip('\n')
	col_p=line_p.split()

	ref_p=col_p[0]
	pos_p=col_p[1]
	cov_p=int(col_p[3])
	seq_p=col_p[4]
	
	num_start=0
	num_end=0

	#Check if seq_p has beginning of SR alignment ('^')
	#if seq_p has contiguous start and end, i.e. "^$", consider it as only start, not both start and end
	if ('^$' in seq_p):
		#num_start=num_start-seq_p.count('^$')
		num_end=num_end-seq_p.count('^$')

	if ('^' in seq_p):
		#Count number of SRs that begin alignment at this position
		num_start=num_start+seq_p.count('^')
		# Store start position in dict
		for ns in range(num_start):
			d_SR_startpos[ref_p].append(pos_p)

	#Check if seq_base has end of SR alignment ('^')
	# if seq_p has '^$', don't consider those as end of SR
	if ('$' in seq_p):
		# count number of SR alignment ends
		num_end=num_end+seq_p.count('$')
		# Store in dict
		for ne in range(num_end):
			d_SR_endpos[ref_p].append(pos_p)



countl=0
# create a dict where key=header and val=corrected ref seq for the position range in the Pileup file
dict_header=defaultdict(list)

# create a list to store last and current positions
# Used to check if contiguous positions, otherwise create a new item in the list (value) of the dict entry
l_checkpos=[]
corr_seq=''
for line in l_pileup:

	#break
	#print line.rstrip('\n')

	# create a dict where key=allele and val=list of its sum of normalized weights across all SRs
	d_allele_listweight=defaultdict(list)

	# Create dict, where key=SR# and val=MAPQ
	d_qualweight={}
	# create dict, where key=SR# and val=edit dist
	d_editweight={}

	#corr_seq=''
	# For each line, create a list to store MAPQ value of each read
	l_MAPQ=[]

	#-------------------------------------------------------------
	# create a dict where key=allele/correction and val=its frequency
	d_allele_freq={}
	#-------------------------------------------------------------

	# create a dictionary to store possible corrections/seq_base
	d_seqbase={}

	corr_base=''

	line=line.rstrip('\n')
	col=line.split()

	ref=col[0]
	pos=col[1]
	ref_base=col[2]
	cov=int(col[3])
	seq_base=col[4]
	
	# Get MAPQ
	col7=col[6]
	for qual in col7:
		# Add +1, since minimum MAPQ can be '0'
		MAPQ=(ord(qual)-33)+1
		l_MAPQ.append(MAPQ)
	Sum_MAPQ=sum(l_MAPQ)
	#-----------------------------------------------------
	# Updated in version 4

	# Check if new ref 
	if ref not in dict_pilepos.keys():
		if (len(dict_pilepos)!=0):	# first ref header
			corr_seq=''

		dict_header[ref].append(corr_seq)
		start=pos
		l_checkpos.append(pos)
		dict_pilepos[ref].append('')
		corr_seq=''

	# ref already exists
	else:
		# Check if ref exists but contiguous positiobn (difference between current and last position==1)
		if (((int(pos)-int(l_checkpos[-1]))==1) or (dict_pilepos[ref][-1]=='')):
			end=l_checkpos[-1]
			align_range=start+'_'+end
			# since pos are in increasing order, check if start pos seen before
			if start in dict_pilepos[ref][-1]:
				dict_pilepos[ref][-1]=align_range # replace with new range having the same start pos but different end pos
				dict_header[ref][-1]=corr_seq
			else:
				dict_pilepos[ref].append(align_range)
				dict_header[ref].append(corr_seq)
			l_checkpos.append(pos)
		
		# If contiguous position => within the same range
		else:
			end=l_checkpos[-1]
			align_range=start+'_'+end
			if start in dict_pilepos[ref][-1]:
				dict_pilepos[ref][-1]=align_range
				dict_header[ref][-1]=corr_seq
			else:
				dict_pilepos[ref].append(align_range)
				dict_header[ref].append(corr_seq)
			l_checkpos.append(pos)
			corr_seq=''
			start=pos
	#-----------------------------------------------------

	# Check if coverage is 1: no need for majority voting
	if (cov==1):		
		if (len(seq_base)==1):

			# Check if match (forward/reverse)
			if ((seq_base=='.') or (seq_base==',')):
				corr_base=ref_base	#match

			elif(re.findall(r'[ACGTNacgtn]+',seq_base)):
				corr_base=seq_base	#mismatch

			elif(seq_base=='*'):
				corr_base=''

			else:
				corr_base=ref_base	# for exceptions like '^)T'
				print 'Exception 1: '+line

		# Cov=1 but insert, delete, start, or stop
		else:
			# Start of sequence
			# Check start of SEQ before insert or delete for cases like '^+.'
			if ('^' in seq_base):
				if (('.' in seq_base) or (',' in seq_base)):
					corr_base=ref_base	#start of seq and match

				elif(re.findall(r'[ACGTNacgtn]',seq_base)):	
					corr_base=re.findall(r'[ACGTNacgtn]+',seq_base)[0]				

			# Check end of SEQ
			elif ('$' in seq_base):
				if (('.' in seq_base) or (',' in seq_base)):
					corr_base=ref_base	
				elif(re.findall(r'[ACGTNacgtn]',seq_base)):
					corr_base=re.findall(r'[ACGTNacgtn]+',seq_base)[0]

			# check for insertion
			elif ('+' in seq_base):
				# For cases like 'c+2at' where ref_base='N'
				insert=re.findall(r'[ACGTNacgtn]+|\+\d+[ACGTN]+|\+\d+[acgtn]+',seq_base)
				if ((len(insert)>1) and ('+' in insert[1])):
					ins_str=re.findall(r'[ACGTN]+|[acgtn]+',insert[1])
					corr_base=insert[0]+ins_str[0]
				else:
					corr_base=insert[0]

			# Check for deletion
			elif ('-' in seq_base):
				# No need to check that base, just replace with ref_base
				corr_base=ref_base	#keep that base and delete the next one (has '*')
				delete=re.findall(r'[ACGTNacgtn]+|\-\d+[ACGTN]+|\-\d+[acgtn]+',seq_base)
				if ((len(delete)>1) and ('-' in delete[1])): 
					del_str=re.findall(r'[ACGTN]+|[acgtn]+',delete[1])
					corr_base=delete[0]

			else:
				corr_base=ref_base
				print 'Exception 2: '+line
			
	# Case of majority vote
	else:
		list_seqbase=[]
		list_numins=[]
		list_newnumins=[]
		list_numdel=[]
		list_newnumdel=[]

		numi_min='1'
		numi_max=''
		numd_min='1'
		numd_max=''

		list_numins=re.findall(r'[ACGTN]\+\d+|[acgtn]\+\d+|\+\d+',seq_base)
		if (len(list_numins)>0):
			# Remove '+'
			for numins in list_numins:
				#num1=int(numins[2:])
				num1=int(numins[1:])
				list_newnumins.append(num1)

			list_newnumins.sort()
			numi_min=str(list_newnumins[0])
			numi_max=str(list_newnumins[-1])
		

		list_numdel=re.findall(r'[ACGTN]\-\d+|[acgtn]\-\d+|\-\d+',seq_base)
		#print list_numdel
		if (len(list_numdel)>0):
			# Remove '-'
			for numdel in list_numdel:
				#num2=int(numdel[2:])
				num2=int(numdel[1:])
				list_newnumdel.append(num2)

			list_newnumdel.sort()	
			numd_min=str(list_newnumdel[0])
			numd_max=str(list_newnumdel[-1])


		list_seqbase=re.findall(r'\.-\d+[ATGCN]{'+numd_min+','+numd_max+'}|\,-\d+[acgtn]{'+numd_min+','+numd_max+'}|\+\d+[ACGTN]{'+numi_min+','+numi_max+'}|\+\d+[acgtn]{'+numi_min+','+numi_max+'}|\-\d+[ACGTN]{'+numd_min+','+numd_max+'}|\-\d+[acgtn]{'+numd_min+','+numd_max+'}|[ACGTN]\+\d+[ACGTN]{'+numi_min+','+numi_max+'}|[acgtn]\+\d+[acgtn]{'+numi_min+','+numi_max+'}|[ACGTN]\-\d+[ACGTN]{'+numd_min+','+numd_max+'}|[acgtn]\-\d+[acgtn]{'+numd_min+','+numd_max+'}|\.\+\d+[ACGTN]{'+numi_min+','+numi_max+'}|\,\+\d+[acgtn]{'+numi_min+','+numi_max+'}|\.|\,|\*|\.\$|\,\$|\^.|\^.\,|[ATGCN]|[acgtn]',seq_base)


		for sb in list_seqbase:
			if '^' in sb:
				list_seqbase.remove(sb)

		# Check if length of seq_base==cov. Allow +/-1
		if (len(list_seqbase)>int(cov)):
			#print 'Error: '+line
			list_Seqbase=list_seqbase[:int(cov)]
			corr_base=ref_base
			

		#---------------------------------------------------------
		# Start - OC
		else:
			# For Quick correction, check frequency
			for allele in list_seqbase:
				#if (allele not in d_allele_freq):
				if (allele not in d_allele_freq.keys()):
					d_allele_freq[allele]=1
				else:
					d_allele_freq[allele]=d_allele_freq[allele]+1

			d_allelefreq_norm={}
			# Calculate normalized freq for each possible correction
			for al in d_allele_freq:
				if al not in d_allelefreq_norm.keys():
					d_allelefreq_norm[al]=d_allele_freq[al]/float(len(list_seqbase))

			#print d_allelefreq_norm
			d_allelefreq_normsort=list(sorted(d_allelefreq_norm, key=d_allelefreq_norm.__getitem__, reverse=True))
			normfreq=d_allelefreq_norm[d_allelefreq_normsort[0]]

			# Check if allele with highest freq has freq > 0.9
			if (normfreq>cutoff_quickcorrect):
				#print 'Consensus'
				max_base=d_allelefreq_normsort[0]
				
			else:

		# End - OC
		#---------------------------------------------------------

				#----------------------------------------------------------------
				#----------------------------------------------------------------
				# Start - OC
				#For an erroneous position in a given read, find the index of SRs that align at that position
				# Create lists to store the start and end positions of the SRs
				l_SR_startpos=[]
				l_SR_endpos=[]
				#Create a list to store the index (i_SR) of SR that align to the error position
				#Size of this list =  num of aligned SRs at that position
				l_SR_index=[]

				#Create a list to store the sum of match-based and MAPQ-based weights
				l_SR_sumweight=[]
				max_index=0
				i_SR=0

				# Get list for a given ref_header
				for ref_header in d_SR_startpos.keys():
					if (ref_header==ref):
						l_SR_startpos=d_SR_startpos[ref_header]
						l_SR_endpos=d_SR_endpos[ref_header]
						
						if (len(l_SR_startpos)!=len(l_SR_endpos)):
							#print 'Not equal'
							diff_pos=abs(len(l_SR_endpos[i_SR:])-len(l_SR_startpos[i_SR:]))
							if (len(l_SR_startpos[i_SR:])<len(l_SR_endpos[i_SR:])):
								if(l_SR_endpos[i_SR]<l_SR_startpos[i_SR]):
									l_SR_endpos=l_SR_endpos[i_SR+diff_pos]
							else:
								l_SR_startpos=l_SR_startpos[i_SR+diff_pos]

						#print len(l_SR_startpos)
						#print len(l_SR_endpos)

						for i_SR in range(min(len(l_SR_startpos),len(l_SR_endpos))):
							#print i_SR
							# Check if pos lies within the start and end range of a SR (SR_i)
							if (int(l_SR_startpos[i_SR])<=int(pos) and int(pos)<=int(l_SR_endpos[i_SR])):
								l_SR_index.append(i_SR)
								sumweight=d_SR_matchnorm[ref_header][i_SR]+d_SR_qual[ref_header][i_SR]
								l_SR_sumweight.append(sumweight)

				#------------------------------------------------------------------------------------
				# Updated in version 6: Don't pick the allele for the SR that has highest sum of normalized weights.
				# Instead check if it is a high-confidence correction

				# For an invalid set
				if (len(l_SR_sumweight)<1):
					#nline='Uneven set\n'+line+'\n'
					#f_pileupiter.write(nline)
					max_base=ref_base
				#if (len(l_SR_sumweight)>0):
				else:
				#----------------------------------------------------------------
				# Added in version 6 - check for low-confidence corrections, keep as it is

					#print list_seqbase
					#print l_SR_sumweight

					# create a dict where key=allele and val=list of its sum of normalized weights across all SRs containing that allele
					for i_al in range(len(list_seqbase)):
						d_allele_listweight[list_seqbase[i_al]].append(l_SR_sumweight[i_al])

					# Create another dict where key=allele and val=its median obtained from d_allele_listweight
					d_allele_median={}

					for k_al in d_allele_listweight.keys():
						d_allele_median[k_al]=median(d_allele_listweight[k_al])

					# Get the two alleles with highest and second-highest median values
					# Sort the dict by value in reverse order
					# output is stored in the format: [(k1, v1), (k2, v2), (k3, v3)], where v1>=v2>=v3
					sorted_d_allele_median=sorted(d_allele_median.items(), key=operator.itemgetter(1), reverse=True)

					# Check if the top two are non-conflicting, i.e. ',' and '.'
					al_highest=sorted_d_allele_median[0][0]
					al_sechighest=sorted_d_allele_median[1][0]

					# No conflicts for these configurations
					if ((al_highest==',' and al_sechighest=='.') or (al_highest=='.' and al_sechighest==',')):
						max_base=al_highest

					else:

						med_highest=sorted_d_allele_median[0][1]
						med_sechighest=sorted_d_allele_median[1][1]

						# Check if low-confidence correction
						#if ((int(med_highest)-int(med_sechighest))<conf_threshold):
						if (int(med_highest)<conf_threshold):
							nline=line+'\n'
							f_pileupiter.write(nline)
							max_base=ref_base
						else:
							max_base=al_highest
				#print l_SR_sumweight
				#print list_seqbase
				#print d_allele_listweight
				#print d_allele_median
				#print sorted_d_allele_median
				#----------------------------------------------------------------

				# Check for start
				if ('^' in max_base):
					if (('.' in max_base) or (',' in max_base)):
						corr_base=ref_base

				# if match
				elif (max_base=='.' or max_base==','):
					corr_base=ref_base

				# check for deletion in next line
				elif ('-' in max_base):
					corr_base=ref_base

				#Check for real deletion
				elif(max_base=='*'):
					corr_base=''

				# check for insertion
				elif ('+' in max_base):
					ins_base=re.findall(r'[ATGCNatgcn]+',max_base)
					temp_ins=''
					for ins in ins_base:
						temp_ins=temp_ins+ins

					if (ref_base=='N' or ref_base=='n'):
						corr_base=temp_ins

					else:
						corr_base=ref_base+temp_ins

				# check for mismatch
				elif(re.findall(r'[ACGTNacgtn]',max_base)):
					corr_base=max_base

				else:
					#nline='Exception 3\n'+line+'\n'
					#f_pileupiter.write(nline)
					corr_base=ref_base
					#print 'Exception 3: '+line


	#print corr_base
	corr_seq=corr_seq+corr_base


#********************************************************************************
# Print corrected reads

# For each ref, keep seq before pos_start of pileup and after pos_end of pileup
# dict_ref may have some headers not found in ppileup file
#for trunc_ref in dict_header.keys():
# Change in v3 -> print all reads for testing with BLASR

for ref in sorted(dict_ref.keys()):

	trunc_ref=ref[1:]
	if (len(trunc_ref)>2):
		if trunc_ref in dict_header.keys():
	#-----------------------------------------
	# Updated in version 4
			# Leftmost start pos
			leftmost_start=int(dict_pilepos[trunc_ref][1].split('_')[0])
			# Rightmost end position
			rightmost_end=int(dict_pilepos[trunc_ref][-1].split('_')[1])

			seq=dict_ref[ref]
			seqcorr_beg=seq[:leftmost_start]
			seqcorr_end=seq[rightmost_end:]

			seqcorr_mid=''
			for i_pos in range(1,len(dict_pilepos[trunc_ref])-1):
				# Get end of curr_range and beg of next_range
				curr_range=dict_pilepos[trunc_ref][i_pos]
				next_range=dict_pilepos[trunc_ref][i_pos+1]
				curr_beg=int(curr_range.split('_')[0])
				curr_end=int(curr_range.split('_')[1])
				next_beg=int(next_range.split('_')[0])

				seqcorr_mid=seqcorr_mid+dict_header[trunc_ref][i_pos]+seq[curr_end:next_beg]

			seqcorr_mid=seqcorr_mid+dict_header[trunc_ref][-1]
			seqcorr=seqcorr_beg+seqcorr_mid+seqcorr_end
			#---------------------------------------
			# Added in version 5 - Remove nonATGCN character
			seqcorr=re.sub(r'\+[\d]+','',seqcorr)
			#---------------------------------------

			print ref
			print seqcorr
	#-----------------------------------------
