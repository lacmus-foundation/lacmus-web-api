using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using API_Identity.Models;
using API_Identity.Models.Repository;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace API_Identity.Controllers
{
    [Route("api/[controller]")]
    [Authorize]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly IUserRepository _repository;

        public UserController(IUserRepository repository)
        {
            _repository = repository;
        }
        // GET api/values
        [HttpGet]
        public async Task<ActionResult<IEnumerable<User>>> Get()
        {
            /*
            var nameIdentifier = this.HttpContext.User.Claims
                .FirstOrDefault(x => x.Type == ClaimTypes.NameIdentifier); */

            var users = await _repository.GetAll();
            if (users == null) {
                return NotFound();
            }
            return Ok(users);
        }

        // GET api/values/5
        [HttpGet("{id}")]
        public async Task<ActionResult<User>> Get(int id)
        {
            var user = await _repository.Get(id);
            if (user == null)
            {
                return NotFound();
            }
            return Ok(user);
        }

        // POST api/values
        [HttpPost]
        public ActionResult<User> Post([FromBody] User user)
        {
            return BadRequest();
        }

        // PUT api/values/
        [HttpPut]
        public async Task<ActionResult<User>> Put([FromBody] User user)
        {
            var newUser = await _repository.Edit(user);
            if (newUser == null)
                return BadRequest("unable to edit user");
            return Ok(newUser);
        }

        // DELETE api/values/5
        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(int id)
        {
            if (await _repository.Remove(id))
                return Ok();
            return BadRequest();
        }
    }
}