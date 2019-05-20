Nutanix Developer Portal Code Samples - Cluster Management
##########################################################

list_vm_v3.cs
.............

Microsoft C# Console application to request a list of all VMs from a specified cluster.  Unlike other samples in this repo, credentials are hard-coded so that our community can get up and running quickly simply copying/pasting this code into their own app (and modifying the IP address/credentials).  Uses **Prism REST API v3** and will work on both Prism Central and Prism Element.

To use this small console app you will require:

- Microsoft Visual Studio (e.g. VS Community_)
- Newtonsoft.Json package for Visual Studio.  Install this in Visual Studio by clicking **View > Other Windows > Package Manager Console** and entering this command:

.. code:: bash

  Install-Package Newtonsoft.Json -Version 12.0.1

- If you create a C# console app called **ConsoleApp1**, you should be able to just copy and paste this file in place of **all** existing code in **Program.cs**, modify the variables and hit run.

.. _Community: https://visualstudio.microsoft.com/downloads/
