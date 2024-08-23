import botocore.exceptions
import boto3
import botocore
import click


session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances=[]
    
    if project:
         filters = [{'Name':'tag:project', 'Values':[project]}] # here we filter by project 
         instances = ec2.instances.filter(Filters=filters) #all our instances
         
    else:
        instances = ec2.instances.all()  
        
    return instances


#-------------THIS IS MAIN GROUP ------------------------------------------------#---------------


@click.group()  # one main group called group 
def cli():
    """Shotty manages Snapshots"""
    
#-------------THIS IS MAIN GROUP ------------------------------------------------#---------------


#-------------THIS IS SNAPSHOT GROUP ------------------------------------------------#---------------

@cli.group('snapshots')   # created to group the commands for volumes
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')  #a pertenece a cli.group('snapshots')  
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True, ## here the code is --all is there list_ would we true , and not the default one
    help="List all snapshots for each volume , not just the most recent")
def list_snapshots(project, list_all):
    "List EC2 VOLUMES"
   
    instances = filter_instances(project)

    for i in instances:
     for v in i.volumes.all():
        for s in v.snapshots.all():
            print(",".join((
                s.id, 
                v.id, 
                i.id,
                s.state,
                s.progress,
                
            )))
            if s.state == 'completed' and not list_all: break  # With this command we only show the most recent snapshots  si es igual a completed and no es ist not_all
            
    return 
    
#-------------THIS IS SNAPSHOT GROUP ------------------------------------------------#---------------

    
#-------------THIS IS Volumes Group ------------------------------------------------#---------------


@cli.group('volumes')   # created to group the commands for volumes
def volumes():
    """Commands for Volumes"""

@volumes.command('list')  #a pertenece a cli.group('instances')  
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 VOLUMES"
   
    instances = filter_instances(project)
    
    for i in instances:
     for v in i.volumes.all():
        print (", ".join ((
        v.id,
        i.id,
        v.state,
        str(v.size) + "GiB",
        v.encrypted and "Encrypted" or "Not Encrypted"
        )))
        
    return

#-------------THIS IS Volumes Group ------------------------------------------------#---------------





#-------------THIS IS Instances Group ------------------------------------------------#---------------

@cli.group('instances') # we created teh group for instaces
def instances():
    "Commands for instances"



############ this is to create snampshot#################
@instances.command('snapshot' , 
        help= " Help to create snapshots of all volumes") # snapshots inside instances to create snapshots 
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshot(project):
    "Create Snapshots for the instances "
    instances = filter_instances(project)
    
    for i in instances:
        print("Stopping VM to snapshots of {0}".format(i.id))
        i.stop()  #stop the vm 
        i.wait_until_stopped()
    
        for v in i.volumes.all():
            print("Creating snapshots of {0}".format(v.id))
            v.create_snapshot(Description="created from Analyzer30000 ")
            
            print("Starting after  snapshots of {0}".format(v.id))  
            
            i.start() 
            i.wait_until_running() #important feature to avoid a mess with the servers
            print("Running server after  snapshots of {0}".format(i.id))  
    return



############ this is to create snampshot#################

@instances.command('list')  #a pertenece a cli.group('instances')  
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List Instances"
   
    instances = filter_instances(project)
        
    for i in instances:
        print(','.join((
           i.id,
           i.state['Name'],
           i.placement['AvailabilityZone']            
        )))
        
    return

@instances.command('stop')  # its a grup that stops the VMs . under click // pertenece a cli.group('instances')
@click.option('--project', default=None,  # now command stop has options like start or stop 
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        print("Stopping {0}" .format(i.id))
       
        try: # in this part is " y try to stop the instance "
            i.stop() #here we send the command to stop 
        except botocore.exceptions.ClientError as e:  # we get the exception and we gave it another name with the e then we print it 
            print("Cloud not stop {0}".format(i.id) + str(e)) # we only catch this exception
            continue
            
    return
    
@instances.command('start')  # its a grup that stops the VMs . under click // pertenece a cli.group('instances')
@click.option('--project', default=None,  # now command stop has options like start or stop 
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        print("Starting {0}" .format(i.id))
        
        try: # in this part is " y try to start the instance "
            i.start() #here we send the command to start 
        except botocore.exceptions.ClientError as e:  # we get the exception and we gave it another name with the e then we print it 
            print("Cloud not start {0}".format(i.id) + str(e)) # we only catch this exception
            continue
    return
#-------------THIS IS Instances Group ------------------------------------------------#---------------
 
    

if __name__ == '__main__':
    cli()
    
    