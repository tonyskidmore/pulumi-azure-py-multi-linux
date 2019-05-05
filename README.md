[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# Azure Multi-Distribution Linux Server example in Python

This example is originally based on the [Azure Web Server example in Python](https://github.com/pulumi/examples/tree/master/azure-py-webserver).  My example use case is to support CI testing of a Linux compliance script (not included) against a number of different Linux VMs.  Initially these distributions will be offers from the Azure Marketplace.  My initial target CI platform will be [Azure DevOps](https://azure.microsoft.com/en-gb/services/devops/) and there is some information already on the Pulumi website [here](https://pulumi.io/reference/cd-azure-devops.html) that should help when it comes to the integration of this project there.

[Pulumi](https://pulumi.io/) looks a very interesting approach to IaC and I like the way that you can use programming language (JavaScipt, TypeScript, Python, Go) constructs rather than trying to use awkward (to me anyway) mechanisms in Terrform, ARM Templates etc. to do things like loops.  

Seeing as this could also be a Terraform project I decided to create the input variables in Terraform format to begin with and use [pyhcl](https://github.com/virtuald/pyhcl) to parse those inputs.  It could have used JSON or YAML for configuration data or just included directly in the Python code.  I have not decided in my thinking yet as whether all configuration should be stored within the script or still maintained outside in the way that Terraform would ingest the HCL variables.  I was considering trying to do the same thing in Terraform after completing the Pulumi side of things, hence the idea of using `variables.tf`.

This test Pulumi project is very much work in progress.

## Python 3

Note that Pulumi requires [Python 3](https://pulumi.io/reference/python.html) as of version 0.16.4 and above.  As my platform of choice is CentOS 7 this is what I did to install a side-by-side installation of Python 3.7.3.  

```
$ sudo yum -y install gcc openssl-devel bzip2-devel libffi-devel wget

$ cd /usr/src
$ sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
$ sudo tar xzf Python-3.7.3.tgz
$ sudo cd Python-3.7.3
$ sudo ./configure --enable-optimizations
$ sudo make altinstall
```
There might be a better way of achieving getting Pulumi to recognize the Python 3.7 program but I just did this:  

```
$ sudo ln -s /usr/local/bin/python3.7 /usr/local/bin/python3
```


## Prerequisites


1. [Install Pulumi](https://pulumi.io/install/)
1. [Configure Pulumi for Azure](https://pulumi.io/quickstart/azure/setup.html)
1. [Configure Pulumi for Python](https://pulumi.io/reference/python.html)

## Deploying and running the program

1. Set up a virtual Python environment and install dependencies

    ```
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

1. Create a new stack:

    ```
    $ pulumi stack init azure-py-multi-linux
    ```

1. Set the Azure environment:

    ```
    $ pulumi config set azure:environment public
    ```

1. Set the required configuration for this example. This example requires you to supply a username and password to
the virtual machine that we are going to create.

    ```
    $ pulumi config set azure-web:username cloud_admin
    ```

    The password is a secret, so we can ask Pulumi to encrypt the configuration:

    ```
    $ pulumi config set --secret azure-web:password Hunter2hunter2
    ```

1. Run `pulumi up` to preview and deploy the changes:

    ```
    $ pulumi update
    Previewing update (azuredev):

        Type                               Name                         Plan       
    +   pulumi:pulumi:Stack                azure-py-webserver-azuredev  create     
    +   ├─ azure:core:ResourceGroup        server                       create     
    +   ├─ azure:network:VirtualNetwork    server-network               create     
    +   ├─ azure:network:PublicIp          server-ip                    create     
    +   ├─ azure:network:Subnet            server-subnet                create     
    +   ├─ azure:network:NetworkInterface  server-nic                   create     
    +   └─ azure:compute:VirtualMachine    server-vm                    create     
    
    Resources:
        + 7 to create

    Do you want to perform this update? yes
    Updating (azuredev):

        Type                               Name                         Status      
    +   pulumi:pulumi:Stack                azure-py-webserver-azuredev  created     
    +   ├─ azure:core:ResourceGroup        server                       created     
    +   ├─ azure:network:VirtualNetwork    server-network               created     
    +   ├─ azure:network:PublicIp          server-ip                    created     
    +   ├─ azure:network:Subnet            server-subnet                created     
    +   ├─ azure:network:NetworkInterface  server-nic                   created     
    +   └─ azure:compute:VirtualMachine    server-vm                    created     
    
    Outputs:
        public_ip: "137.117.15.111"

    Resources:
        + 7 created

    Duration: 2m55s

    ```

1. Get the IP address of the newly-created instance from the stack's outputs: 

    ```
    $ pulumi stack output public_ip
    137.117.15.111
    ```

1. Check to see that your server is now running:

    ```
    $ curl http://$(pulumi stack output public_ip)
    Hello, World!
    ```

1. Destroy the stack:

    ```
    ▶ pulumi destroy --yes
    Previewing destroy (azuredev):

        Type                               Name                         Plan       
    -   pulumi:pulumi:Stack                azure-py-webserver-azuredev  delete     
    -   ├─ azure:compute:VirtualMachine    server-vm                    delete     
    -   ├─ azure:network:NetworkInterface  server-nic                   delete     
    -   ├─ azure:network:Subnet            server-subnet                delete     
    -   ├─ azure:network:PublicIp          server-ip                    delete     
    -   ├─ azure:network:VirtualNetwork    server-network               delete     
    -   └─ azure:core:ResourceGroup        server                       delete     
    
    Resources:
        - 7 to delete

    Destroying (azuredev):

        Type                               Name                         Status      
    -   pulumi:pulumi:Stack                azure-py-webserver-azuredev  deleted     
    -   ├─ azure:compute:VirtualMachine    server-vm                    deleted     
    -   ├─ azure:network:NetworkInterface  server-nic                   deleted     
    -   ├─ azure:network:Subnet            server-subnet                deleted     
    -   ├─ azure:network:VirtualNetwork    server-network               deleted     
    -   ├─ azure:network:PublicIp          server-ip                    deleted     
    -   └─ azure:core:ResourceGroup        server                       deleted     
    
    Resources:
        - 7 deleted

    Duration: 3m49s

    ```
