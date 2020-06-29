using System;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using System.IdentityModel.Tokens.Jwt;
using Identity.Models;
using Identity.Models.Repository;
using Identity.Models.Tokens;
using Identity.ViewModels;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;


namespace Identity.Controllers
{
    public class AuthController : Controller
    {
        private readonly IUserRepository _repository;
        private readonly IConfiguration _configuration;
        private readonly IPasswordHasher _passwordHasher;
        private readonly ITokenService _tokenService;

        public AuthController(IUserRepository repository, IConfiguration configuration, IPasswordHasher passwordHasher, ITokenService tokenService)
        {
            _repository = repository;
            _configuration = configuration;
            _passwordHasher = passwordHasher;
            _tokenService = tokenService;
        }

        [Route("register")]
        [AllowAnonymous]
        [HttpPost]
        public async Task<ActionResult> InsertUser([FromBody] RegisterViewModel model)
        {
            if (await _repository.GetByEmail(model.Email) != null)
                return BadRequest("user already exists");
            
            var user = new User()
            {
                Email = model.Email,
                Phone = model.Phone,
                FirstName = model.FirstName,
                LastName = model.LastName,
                PasswordHash = _passwordHasher.GenerateIdentityV3Hash(model.Password)
            };
            if(await _repository.Add(user) != null)
                return Ok(user);
            return BadRequest("unable to add user");
        }

        [Route("login")]
        [AllowAnonymous]
        [HttpPost]
        public async Task<ActionResult> Login([FromBody] LoginViewModel model, 
            [FromServices] IJwtSigningEncodingKey signingEncodingKey,
            [FromServices] IJwtEncryptingEncodingKey encryptingEncodingKey)
        {
            var user = await _repository.GetByEmail(model.Email);
            if (user == null || !_passwordHasher.VerifyIdentityV3Hash(model.Password, user.PasswordHash))
                return Unauthorized();

            var usersClaims = new [] 
            {
                new Claim(ClaimTypes.Name, user.Email),                
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString())
            };
            
            var jwtToken = _tokenService.GenerateAccessToken(usersClaims, signingEncodingKey, encryptingEncodingKey);
            var refreshToken = _tokenService.GenerateRefreshToken();

            return Ok(
                new
                {
                    token = jwtToken,
                    refreshToken = refreshToken
                });
        }
    }
}