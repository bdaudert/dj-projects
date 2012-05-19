// ---------------------------------------------
// --- Name:    Easy DHTML Treeview           --
// --- Author:  D.D. de Kerf                  --
// --- Version: 0.1           Date: 6-6-2001  --
// ---------------------------------------------
function Toggle(node)
{
	// Unfold the branch if it isn't visible
	if (node.nextSibling.style.display == 'none')
	{
		// Change the image (if there is an image)
		if (node.children.length > 0)
		{
			if (node.children.item(0).tagName == "IMG")
			{
				node.children.item(0).src = "{{MEDIA_URL}}/img/minus.gif";
			}
		}

		node.nextSibling.style.display = '';
	}
	// Collapse the branch if it IS visible
	else
	{
		// Change the image (if there is an image)
		if (node.children.length > 0)
		{
			if (node.children.item(0).tagName == "IMG")
			{
				node.children.item(0).src = "plus.gif";
			}
		}

		node.nextSibling.style.display = 'none';
	}

}
