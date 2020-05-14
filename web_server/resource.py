from pathlib import Path

FILE_EXTENSION_TO_MIME = {
	'.html': 'text/html',
	'.css': 'text/css',
	'.json': 'application/json',
}

class HttpResource:
	"""Container for HTTP response content"""

	@classmethod
	def get_resource(cls, base_dir, path):
		"""Creates a new HttpResource object based on the base directory and the requested path"""

		body = ''
		is_requested_resource = False

		base_dir = Path(base_dir)
		target_path = base_dir / Path(path[1:] if path != '/' else '/index.html')
		target_path.resolve()

		if base_dir in target_path.parents:
			if target_path.suffix == '':
				target_path = target_path.with_suffix('.html')

			if target_path.is_file():
				with target_path.open() as f:
					body = f.read()
					is_requested_resource = True

		return HttpResource(body or '404: Not Found', target_path.suffix), is_requested_resource

	def __init__(self, content='', ext=None):

		self.content = content.encode()
		self.mime = FILE_EXTENSION_TO_MIME.get(ext, 'text/html')
		self.content_length = len(self.content)

		if self.content:
			self.associated_headers = {
				'Content-Type': self.mime,
				'Content-Length': self.content_length,
			}
		else:
			self.associated_headers = {}