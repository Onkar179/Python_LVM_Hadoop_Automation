import os 
import getpass

os.system("tput setaf 3")
print("\t\t\t***********Welcome To My Automation Tool*******************")
os.system("tput setaf 7")
print("\t\t\t-------------------------")

passwd = getpass.getpass("Enter your password : ")

if passwd == "onkar":
    print("\n\t\t-----------------> you have sucessfully logged in <--------------------------")
else:
    print("Wrong password")
    exit()

r = input("\n\t\t Select your workspace --> (local/remote) : ")

if r == "remote":
    ip = input("\n\t\t\tEnter Remote IP: ")
while True:
       print("\n************************************** Menu List ************************************************")
       print("""
\n\t\t
Press 1: Run Date Command
press 2: Install Hadoop Requirements
press 3: Configure Hadoop Name / Data Node
press 4: Start & check the status of Hadoop services
press 5: Create A LVM Partition
press 6: Mount the LVM Partiton
press 7: Extend the size of LVM Partitions
press 8: Add New Hard Disk to Volume Group (LVM) 
""")
       ch = input("\n\t\t\t\tEnter your choice: ")


       if r == "local":
           if int(ch) == 1:
               os.system('date')
           elif int(ch) == 2:
               os.system('cal')
           elif int(ch) == 3:
               os.system('rpm -i jdk-8u171-linux-x64.rpm')

       elif r == "remote":
           if int(ch) == 1:
               os.system('ssh {} date'.format(ip))
           elif int(ch) == 2:
               os.system('ssh {} rpm -ivh jdk-8u171-linux-x64.rpm'.format(ip))
               print("-------------------------------------------------------------------------")
               print("\n\t\t\tJava Software Sucessfully Installed ....")
               print("-------------------------------------------------------------------------")
               print("\n\t\t\tHadoop Software Sucessfully Installed ....") 
               os.system('ssh {} rpm -ivh hadoop-1.2.1-1.x86_64.rpm --force'.format(ip))
           elif int(ch) == 3:
               op = input("Configure Your System as ? (Name / Data): ")
               dir = input("\n\t\tEnter your data node directory name : ")
               print("\t\t\t\tConfiguring hdfs-site.xml file ............")
               os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/hdfs-site.xml")
               os.system("echo -e '\n<!-- Put site-specific property overrides in this file. -->' >> /root/hdfs-site.xml")
               os.system('echo -e "\n<configuration>" >> /root/hdfs-site.xml')
               os.system('echo -e "\n<property>" >> /root/hdfs-site.xml')
               os.system('echo -e "<name>dfs.data.dir</name>" >> /root/hdfs-site.xml')
               os.system('echo -e "<value>{}</value>" >> /root/hdfs-site.xml'.format(dir))
               os.system('echo -e "</property>" >> /root/hdfs-site.xml')
               os.system('echo -e "\n</configuration>" >> /root/hdfs-site.xml')
               os.system('scp /root/hdfs-site.xml {}:/etc/hadoop'.format(ip))
               print()
               print()
               nip = input("Enter Name Node IP :")
               print("\t\t\t\tConfiguring core-site.xml file ...........")
               os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/core-site.xml")
               os.system('echo -e "\n<!-- Put site-specific property overrides in this file. -->" >> /root/core-site.xml')
               os.system('echo -e "\n<configuration>" >> /root/core-site.xml')
               os.system('echo -e "\n<property>" >> /root/core-site.xml')
               os.system('echo -e "<name>fs.default.name</name>" >> /root/core-site.xml')
               os.system('echo -e "<value>hdfs://{}</value>" >> /root/core-site.xml'.format(nip))
               os.system('echo -e "</property>" >> /root/core-site.xml')
               os.system('echo -e "\n</configuration>" >> /root/core-site.xml')
               os.system('scp /root/core-site.xml {}:/etc/hadoop'.format(ip))
           elif int(ch) == 4:
               print("\n\n\t\t\t\t\tstarting hadoop data node services .........")
               os.system('ssh {} hadoop-daemon.sh start datanode'.format(ip))
               print()
               os.system('ssh {} hadoop dfsadmin -report'.format(ip))
           elif int(ch) == 5:
               dev = input("\t\t\t\tEnter Your Device Name : ")
               os.system('ssh {} pvcreate {}'.format(ip , dev))
               print("\t\t\tSucessfully Created pv : {}".format(dev))
               os.system('ssh {} pvdisplay {}'.format(ip , dev))
               print("------------------------------------------------------")
               vg = input("\t\t\t\tEnter The Name of Volume Group : ")
               os.system('ssh {} vgcreate {}  {}'.format(ip , vg , dev))
               os.system('ssh {} vgdisplay {}'.format(ip , vg))
               print("------------------------------------------------------")
               lv = input("\t\t\t\tEnter Your Logical Volume Name : ")
               sz = input("\t\t\t\tEnter the Size of Partition you want : ")
               os.system('ssh {} lvcreate --size {} --name {} {}'.format(ip , sz , lv ,vg))
               os.system("ssh {} lvdisplay {}/{}".format(ip , vg ,lv))
               print("------------------------------------------------------")
               os.system('ssh {} mkfs.ext4 /dev/{}/{}'.format(ip ,vg , lv))
               print("\t\t\tLogical Volume Sucessfully Formatted ..")
               
           elif int(ch) == 6:
               fold = input("\t\tEnter your folder Name which you want to mount on LVM Parition : ")
               vg = input("\t\tEnter Volume Group Name : ")
               lv = input("\t\tEnter Logical Volume Name : ")
               os.system("ssh {} mount /dev/{}/{}  {}".format(ip , vg , lv , fold))
               print("\t\t\tSucessfully Mounted the LVM Partiton ..")
               os.system('ssh {} df -hT'.format(ip))

           elif int(ch) == 7:
               ex = input("\t\tHow much you want to Extend the LVM Partition? : ")
               vg = input("\t\tEnter Volume Group Name : ")
               lv = input("\t\tEnter Logical Volume Name : ")
               os.system('ssh {} lvextend --size {} /dev/{}/{}'.format(ip , ex , vg , lv))
               print("\t\t\tSucessfully Extended the Size of LVM Partition ")
               os.system('ssh {} resize2fs  /dev/{}/{}'.format(ip , vg ,lv))
               os.system('ssh {} df -hT'.format(ip))

           elif int(ch) == 8:
               nw = input("\t\tEnter the Name of Device you want to Add in Volume Group (LVM) : ")
               vg = input("\t\tEnter Volume Group Name : ")
               os.system('ssh {} vgextend {} {}'.format(ip , vg , nw))
               print("\t\tDynamically Added Extra Storage or Volume in LVM")
               print("-------------------------------------------------------------------")
               os.system('ssh {} vgdisplay {}'.format(ip , vg))



 
               
               
               
    






                     

