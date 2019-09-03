import copy

class Blupdate:
    """
    This class represents an update in the base layer. It is used to recompute the existing layers into the new base layer.

    When you want to update the base layer to a new text, initialize the class with the content of the old base layer and the new one.
    Then for each annotation in the layers, you can call get_updated_coord() with the coordinate of the annotation, it will return the
    updated coordinate that you can use to update the annotation.
    """

    def __init__(self, srcbl, dstbl):
        self.srcbl = srcbl
        self.dstbl = dstbl
        self.cctv = self.compute_cctv
        self.contextlen = 16

    @staticmethod
    def compute_cctv(self):
        """
        Computes a cctv from self.srcbl to self.dstbl. This will take some effort but should be reasonable with DMP.
		
		The cctv should the a list of triples, each triple being:
		  - char start in srcbl (int)
		  - char end in srcbl (int)
		  - char coord diff to the corresponding range in dstbl (int)


		It indicates the areas where no change has occured between srcbl and dstbl and where a simple character
		coordinate translation is possible without looking at the context.

		Here's an example:

		srcbl = abefghijkl
		dstbl = abcdefgkl

		the result will be:
		[
			(0,2,0),
			(2,5,2),
			(8,10,-1)
		]

		meaning in plain English:
			- from character 0 to 2 in srcbl (meaning "ab"), no character coordinate translation is needed for the equivalent area in dstbl
			- from character 2 to 5 in srcbl (meaning "efg"), character coordinates in srcbl need to be added +2 in order to get their equivalent in dstbl
			- from character 8 to 10 in srcbl (meaning "kl"), character coordinates in srcbl need to be added -1 in order to get their equivalent in dstbl

        """
        pass

    def get_cctv_for_coord(self, srcblcoord):
    	"""
    	Returns the character coordinate in dstbl for a character coordinate in srcbl according to the cctv. It returns two arguments:
    	  - the character coordinate translation, or an estimate if undefined
    	  - a boolean: true if the character coordinate is certain, false if it's an estimate

		In the relevant case, the estimate is computed by taking the average of the cctv value for the range before and for the range after.
		For example in the same example if we want the estimate for srcblcoord = 6, we see that for character coords [2-5] we have 2 and for [8-10] we have -1,
		the estimate will be 2+(-1) / 2 = 0.5, for which we take an int value: 1.

		So for a more complete example we would have:
		  get_cctv_for_coord(3) == (2, true)
		  get_cctv_for_coord(7) == (1, false)
    	"""
    	pass

    def get_context(self, srcblcoord):
    	"""
		This returns the left and right context of a character coordinate in srcbl, in the form of a tuple with two strings.
		The length of the context is set by self.contextlen.

		For instance:
		   get_context(3) == ("abe", "fgh")
    	"""
    	pass

    def dmp_find(self, context, dstcoordestimate):
    	"""
		This function uses the dmp lib wizardry to get the a coordinate in dstbl that is:
		  - around dstcoordestimate
		  - approximately surrounded by context

		This is conceptually simple but might require the most time as it might require understanding the dmp code to
		hook into private functions.
    	"""
    	pass

    def get_updated_with_dmp(self, srcblcoord, cct):
    	"""
    	This returns the coordinate in dstbl corresponding to srcblcoord using the dmp methods, and an indication from the cctv.

    	By convention, the function returns -1 when it is unable to compute the new coordinate.
    	"""
    	context = self.get_context(srcblcoord)
    	dstcoordestimate = srcblcoord+cct
    	return self.dmp_find(context, dstcoordestimate)

    def get_updated_coord(self, srcblcoord):
    	"""
    	This is the main function used to update annotations. Annotations have references to character coordinates in a specific base layer. This function
    	allows them to get the corresponding coordinate in the new base layer.

    	By convention, the return value -1 means that the function is unable to compute the new coordinate.
    	"""
    	cctvforcoord = self.get_cctv_for_coord(srcblcoord)
    	if cctvforcoord[1]:
    		return srcblcoord+cctvforcoord[0]
    	else:
    		return self.getupdatedwithdmp(srcblcoord, cctvforcoord[0])