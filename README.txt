this project contains a simple app called "Task Manager".
	* task manager is a system to define task for a project. edit and delete tasks by the owner. 
	* each loged in user can add tasks to the project by their own username and add a status to it.
	* each user can edit and delete tasks that owns. 
	* each user only can view tasks details that doesn't own, without any permission to edit delete. 
	
	
	SUPER USER: 
		username: admin1 password: admin1234
		username: admin2 password: admin1234


	Models : 
			
		Task:
			title (charfield)
			description (charfield)
			status (IntegerField)  #choices : 1-started 2-processing 3-pending 4-ended 
			owner (foreignKey - setting.AUTH_USER_MODEL)
			created_at (date)
			updated_at (date)
		
		User :
			django's default supperuser model. 


	URLs :
		 request: GET '' 
		 response: task_list, task_list.html
		 description: renders an html file with list of all tasks.
		 
		 request: GET 'taskManager/task/create'
		 response: form, task_form.html
		 description: renders html file with CreateTaskForm
		 
		 request: POST 'taskManager/task/create'
		 response (if form invalid): form, task_form.html
		 response (if form valid) :all_task.html
		 description : renders form if given form is invalid. saves new task and returns to all tasks page, return.
		 
		 request: GET 'taskManager/task/task_pk' , pk 
		 response: task_detail.html , task
		 description: renders html file for tasks information. returns 404 if task with pk was not found. 		 


		 request: GET 'taskManager/task/update/task_pk' , pk
		 response: form, task_form.html
		 description: renders html file with CreateTaskForm with given task .
		 
		 request: POST 'taskManager/task/update/task_pk' , pk
		 response (if form invalid): form, task_form.html
		 response (if form valid) :task_list.html
		 description: renders form if given form is invalid. saves updated task and returns to all tasks page, return 404 if pk not found.
		 
		request: GET 'taskManager/task/delete/task_pk' , pk 
		response: task_confirm_delete.html
		description: checks if user is authenticated. returns 404 if task with pk was not found.
		
		request: POST 'taskManager/task/delete/task_pk' , pk 
		response: task_list.html
		description: if confirm/ deletes task and returns to all tasks page. if not conirm/ does nothing and returns to all tasks page. 
		
		
		
	
	TEMPLATEs :
				
		task_list.html
			extends: "base_bootstrap.html"
			ctx : task_list, strval
			
		task_confirm_delete
			extends: "base_bootstrap.html"
			ctx : task
			**checks user authentication.
			
		task_detail.html
			extends: "base_bootstrap.html"
			ctx : task
			
			
		task_form.html
			extends : "base_bootstrap.html" 
			load: crispy_forms_tags
			ctx : form (CreateTaskForm) , project (attached to task)
			**checks user authentication.


	Project On Server:
		https://soroormonzavi.pythonanywhere.com/
	
	
		
		
		