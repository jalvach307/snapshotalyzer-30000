import boto3
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
def list_volumes(project):
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

@instances.command('snapshot' , 
        help= " Help to create snapshots of all volumes") # snapshots inside instances to create snapshots 
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshot(project):
    "Create Snapshots for the instances "
    instances = filter_instances(project)
    
    for i in instances:
    
        for v in i.volumes.all():
            print("Creating snapshots of {0}".format(v.id))
            v.create_snapshot(Description="created from Analyzer30000 ")
    

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
        i.stop() #here we send the command to stop 
        
    return
    
@instances.command('start')  # its a grup that stops the VMs . under click // pertenece a cli.group('instances')
@click.option('--project', default=None,  # now command stop has options like start or stop 
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        print("Starting {0}" .format(i.id))
        i.start() #here we send the command to stop 
        
    return
#-------------THIS IS Instances Group ------------------------------------------------#---------------
 
    

if __name__ == '__main__':
    cli()
    
    