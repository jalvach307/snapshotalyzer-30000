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

@click.group() # we created teh group 
def instances():
    "Commands for instances"
    
@instances.command('list')  #antes eras click.command and we gave it name lists  
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

@instances.command('stop')  # its a grup that stops the VMs . under click 
@click.option('--project', default=None,  # now command stop has options like start or stop 
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        print("Stopping {0}" .format(i.id))
        i.stop() #here we send the command to stop 
        
    return
    
@instances.command('start')  # its a grup that stops the VMs . under click 
@click.option('--project', default=None,  # now command stop has options like start or stop 
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    
    instances = filter_instances(project)
        
    for i in instances:
        print("Starting {0}" .format(i.id))
        i.start() #here we send the command to stop 
        
    return
    
    

if __name__ == '__main__':
    instances()
    
    