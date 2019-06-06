Nutanix Developer Portal Code Samples - C#
##########################################

To use the C# code samples, the following environment is recommended.

- Visual Studio Community_ (free & recommended) or full Visual Studio (commercial software)
- Access to a Nutanix Cluster for API testing purposes.
- Nutanix Community Edition is supported but may not always provide the exact same APIs as a "full" Nutanix cluster.
- The Newtonsoft.Json extension for .NET.  To install Newtonsoft.Json, please see the official documentation_.  **This will need to be done before continuing below**.

.. note:: Please note that instructions provided in this repository will assume the use of Visual Studio Community software.

Console Applications
....................

The provided C# console applications are designed to demonstrate use of the Nutanix Prism REST APIs from C#.  To use the samples in your environment, please follow the instructions below.

The examples and screenshots below are from the **list_vm_v3.cs** sample.

#. Open Visual Studio Community_
#. Select **Create a new project**

   .. figure:: new_project.png

#. Select **Console App (.NET Framework)** from the list of options (it may be easier to search for **console** in the search bar)

   .. figure:: new_console_app.png

#. Click **Next** and configure the app as appropriate for your environment (example shown below).

   .. figure:: configure_console_app.png

#. Click **Create**

#. When the new console application is created, the default Program.cs contents can be completely replaced with the code from the repository sample you are using.

#. In the default sample code, edit the **Parameters** object so that the **URI**, **Username** and **Password** are correct for your environment.

#. Either build (Ctrl-Shift-B) or run (F5) the application.  The complete JSON response will be shown in the console application window.

   .. figure:: app_running.png

.. _Community: https://visualstudio.microsoft.com/vs/community/
.. _Documentation: https://www.nuget.org/packages/Newtonsoft.Json/
