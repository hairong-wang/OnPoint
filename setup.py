
from distutils.core import setup
setup(
  name = 'onpoint',         # How you named your package folder (MyLib)
  packages = ['onpoint'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'NLP question answering service',   # Give a short description about your library
  author = 'Hairong Wang',                   # Type in your name
  author_email = 'whairong2011@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hairong-wang/OnPoint',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hairong-wang/OnPoint/archive/v_06.tar.gz',    # I explain this later on
  keywords = ['NLP', 'question-answering_service', 'Flask-app'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'tensorflow',
          'absl-py',
          'nltk'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
