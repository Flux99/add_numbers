from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Distributed Job Scheduler System')

# Nodes representing components in the system
dot.node('A', 'Scheduler Node')
dot.node('B', 'Cron Jobs Table')
dot.node('C', 'Scheduled Tasks Table')
dot.node('D', 'DAG Table')
dot.node('E', 'Executor')
dot.node('F', 'S3 Storage (Binary Files)')
dot.node('G', 'Message Broker (ActiveMQ)')
dot.node('H', 'Read-Only Replicas')
dot.node('I', 'Change Data Capture (Kafka)')
dot.node('J', 'Zookeeper (Distributed Locks)')

# Add edges to show interactions
dot.edge('A', 'B', label='Reads cron schedules')
dot.edge('A', 'C', label='Schedules tasks based on cron jobs')
dot.edge('A', 'D', label='Reads DAG job definitions')
dot.edge('A', 'E', label='Assigns jobs to executors')
dot.edge('A', 'G', label='Queues jobs')
dot.edge('E', 'F', label='Fetches binaries for execution')
dot.edge('E', 'H', label='Checks job status (read-only)')
dot.edge('A', 'I', label='Updates with job status via Kafka')
dot.edge('J', 'A', label='Prevents duplicate task execution')

# Add extra edges to show relationships for load balancing and retries
dot.edge('G', 'E', label='Message Broker routes jobs to executors')
dot.edge('E', 'F', label='Fetch binaries for tasks')
dot.edge('C', 'I', label='Change Data Capture updates')
dot.edge('E', 'J', label='Handles retries and job locks')

# Render the diagram to a file
dot.render('distributed_job_scheduler_system', format='png', view=True)
