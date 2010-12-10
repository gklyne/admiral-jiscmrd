/**
 * @fileoverview
 * Read from the admiral manifest if any exists and populate form fields and provide a directory listing for selection.
 * Create a manifest if one does not exist.
 * 
 * 
 * @author Bhavana Ananda
 * @version $Id: $
 * 
 * Coypyright (C) 2010, University of Oxford
 *
 * Licensed under the MIT License.  You may obtain a copy of the License at:
 *
 *     http://www.opensource.org/licenses/mit-license.php
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Read from the admiral manifest if any exists and populate form fields and provide a directory listing for selection.
 */
jQuery(document).ready( function ()
{
   url = document.URL;
   
   // Get Dir value from the url to display as default and get metadata information for the dataset dir
   var dir = url.split("=");
   
   if(dir.length>1)
   {   
       // Display all the form fields associated with the directory supplied in the url
       displayValues(dir[1]);
   }
                           
   var m = new admiral.AsyncComputation();
   
   m.eval(function(value,callback)
   {   // Execute the dataset listing logic
       admiral.displayDirectories(callback);           
   });
    
   m.eval(function(value,callback)
   {                    
       // Populate directory listing box with results received
       jQuery("#dirlist").empty();
       
       for (i=0; i<value.length; i++)
       {  
           newjelem='<span class="dirlistitem">'+value[i]+'</span>';
           jQuery("#dirlist").append(newjelem);
       }
        callback(value);
   });    
   
   m.eval(function(value, callback)
   {
       // Set click handlers on directory items
       jQuery("#dirlist > .dirlistitem").click( function()
       {  
           // Display all the form fields associated with the directory selected from the list 
           displayValues(jQuery(this).text());                    
       });
   }); 
                       
   m.exec(null,admiral.noop);
});       


/**
 * Read from the admiral manifest and display the form fields.
 * 
 * @param directorySelected   Directory name for which the ADMIRAL metadata needs to be extracted.
 * @param callback            Callback function.
 */
function displayValues(directorySelected,callback)
{       
      var n = new admiral.AsyncComputation(); 
      n.eval(function(directorySelected,callback)
      { 
           jQuery("#datDir").val(directorySelected);
           // Get the manifest informaton from the server for display
           admiral.getMetadata(directorySelected,callback); 
      });
     
      // Populate the other fields with the value received
      n.eval(function(formValues,callback)
      {                                 
           jQuery("#datId").val(formValues["identifier"]);
           jQuery("#description").val(formValues["description"]);
           jQuery("#title").val(formValues["title"]);      
      });    
      
      n.exec( directorySelected,admiral.noop);          
}  
                                 