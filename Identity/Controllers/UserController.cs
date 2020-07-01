using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Identity.Models.User;
using Identity.ViewModels.User;
using Microsoft.AspNetCore.Mvc;

namespace Identity.Controllers
{
    [Route("api/v1/user")]
    public class UserController : Controller
    {
        // TODO: Получить список всех пользователей
        [HttpGet]
        public async Task<ActionResult<IEnumerable<IUser>>> Get()
        {
            throw new NotImplementedException();
        }
        
        // TODO: Получить информацию о конкретном мользователе
        [HttpGet("{id}")]
        public async Task<ActionResult<IUser>> Get(int id)
        {
            throw new NotImplementedException();
        }

        // TODO: Создать нового пользователя
        [HttpPost]
        public ActionResult<IUser> Post([FromBody] SignUpViewModel model)
        {
            throw new NotImplementedException();
        }

        // TODO: Обновить инфу о пользователе
        [HttpPut]
        public async Task<ActionResult<IUser>> Put([FromBody] UpdateUserViewModel model)
        {
            throw new NotImplementedException();
        }

        // TODO: Удалить пользователя
        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(int id)
        {
            throw new NotImplementedException();
        }
    }
}