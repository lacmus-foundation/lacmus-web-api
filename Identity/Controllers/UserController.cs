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
        [HttpGet("{id}/{fromId}")]
        public async Task<ActionResult<IUser>> Get(ulong id, ulong fromId)
        {
            Console.WriteLine($"{id} - {fromId}"); // for debug
            return Ok();
        }

        // TODO: Создать нового пользователя
        [HttpPost]
        public ActionResult<IUser> Post([FromBody] SignUpViewModel model)
        {
            throw new NotImplementedException();
        }

        // TODO: Обновить инфу о пользователе
        [HttpPut("{fromId}")]
        public async Task<ActionResult<IUser>> Put([FromBody] UpdateUserViewModel model, ulong fromId)
        {
            throw new NotImplementedException();
        }

        // TODO: Удалить пользователя
        [HttpDelete("{id}/{fromId}")]
        public async Task<ActionResult> Delete(ulong id, ulong fromId)
        {
            throw new NotImplementedException();
        }
    }
}