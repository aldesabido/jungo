from ...forms.orders import *
from ...models.orders import *
from ...models.orders_misc import *
from ...views.common import *


import os,zipfile,StringIO

def docs_dialog(request):
	return render(request, 'orders/dialogs/docs_dialog.html')

def upload(request,order_id = None):
	try:
		files = request.FILES if request.FILES else []


		if len(files) == 0:
			raise_error("Kindly select a attachment first.")

		for name in files:
			uploadfile = files[name]
			data = {"order": order_id,"created_by": request.user.id,}
			file = {}
			data["filename"] = uploadfile
			file["filelocation"] = uploadfile


			order_document_form = Order_document_form(data,file)
			if order_document_form.is_valid():
				order_document_save = order_document_form.save()
			else:
				raise_error(order_document_form.errors,True)
				
		return success()
	except Exception as e:
		return error(e)

def read(request,order_id):
	try:
		try:
			order_instance = Order.objects.get(id = order_id)
			docs = order_instance.get_docs()
			return success_list(docs)
		except Order.DoesNotExist:
			raise_error("Order doesn't exists.")
	except Exception as e:
		raise e

def remove(request,order_id,pid):
	try:
		try:
			data = post_data(request)
			order_instance = Order.objects.get(id = order_id,client = request.user.id)
			try:
				order_document_instance = Order_document.objects.get(id = pid)
				order_document_instance.delete()

				return success("Note successfully deleted.")
			except Order_document.DoesNotExist:
				raise_error("Note not found.")
		except Order.DoesNotExist:
			raise_error("Order not found.")
	except Exception as e:
		return error(e)

def download(request,order_id,pid):
	try:
		try:
			data = post_data(request)
			order_instance = Order.objects.get(id = order_id,client = request.user.id)
			try:
				order_document_instance = Order_document.objects.get(id = pid)
				filepath = order_document_instance.get_url()
				response = HttpResponse(content_type='application/force-download')
				response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=order_document_instance.filename)
				response['X-Sendfile'] = smart_str(filepath)
				response.write(open(filepath).read())
				return response
			except Order_document.DoesNotExist:
				raise_error("Note not found.")
		except Order.DoesNotExist:
			raise_error("Order not found.")
	except Exception as e:
		return error(e)

def batch_download(request,order_id):
	try:
		try:
			data = post_data(request)
			instance = Order.objects.get(id = order_id,client = request.user.id)
			foldername = instance.filename("Documents")

			files = instance.get_docs()

			# Folder name in ZIP archive which contains the above files
		    # E.g [thearchive.zip]/somefiles/file2.txt
		    # FIXME: Set this to something better
			zip_filename = "%s.zip" % foldername
			# Open StringIO to grab in-memory ZIP contents
			s = StringIO.StringIO()

			# The zip compressor
			zf = zipfile.ZipFile(s, "w")
			for file in files:
				# Calculate path for file in zip
				fdir, fname = os.path.split(file["url"])
				zip_path = os.path.join(foldername, file["filename"])

				# Add file, at correct path
				zf.write(file["url"], zip_path)

			# Must close zip for all contents to be written
			zf.close()
			# Grab ZIP file from in-memory, make response with correct MIME-type
			resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
			# ..and correct content-disposition
			resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

			return resp
			
		except Order.DoesNotExist:
			raise_error("Order not found.")
	except Exception as e:
		return error(e)