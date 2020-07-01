using System;
using System.Collections.Generic;
using Identity.Models.Token;
using Identity.ViewModels.Token;
using Identity.ViewModels.User;
using Microsoft.AspNetCore.Mvc;

namespace Identity.Controllers
{
    [Route("api/v1/token")]
    [ApiController]
    public class TokenController : Controller
    {
/* TODO: user login
        1 Провалидировать данные пользоватея (лог\пасс) и добыть информацию о нем о нем (роли) из Postgress
        2 Выдать новый токен (в открытом виде)
        
    Полезные ссылки:
            - https://www.krakend.io/docs/authorization/jwt-signing/
            - https://ru.wikipedia.org/wiki/JSON_Web_Token

    curl -X POST --data '{"email":"gosha20777@lacmus.org","password":"pass"}' https://localhost:5000/api/v1/token
        {
            "access_token": {
                "aud": "https://api.lacmus.org",           (str)    == всегда одно и тоже (кем выдан токен)
                "iss": "https://lacmus.org",               (str)    == пусть будет тоже одиноковым (кому токен выдан)
                "sub": "1234567890qwertyuio",              (str)    == id пользователя в бд
                "jti": "mnb23vcsrt756yuiomnbvcx98ertyuiop",(str)    == id сессии, случайный хеш сесии, каждый раз новый
                "roles": ["user", "admin"],                (str)    == роли пользователя в бд
                "exp": 1735689600                          (uint64) == время жизни в формате UNIX TIME (30 мин думаю будет нормас)
            },
            "exp": 1735689600,
            "user_id": "1234567890qwertyuio"
        }
*/
        [HttpPost]
        public ActionResult<TokenIssuer> GetToken([FromBody] LogInViewModel model)
        {
            Console.WriteLine($"LogIn\n\temail: {model.Email}\n\tpass:{model.Password}");
            UInt64 exp = 1735689600;
            var aud = "https://lacmus.io";
            var iss = "https://lacmus";
            var sub = "1234567890qwertyuio";
            var jti = "mnb23vcsrt756yuiomnbvcx98ertyuiop";
            var roles = new List<string>(new []{ "user", "admin" });
            
            var tokenIssuer = new TokenIssuer();
            tokenIssuer.AccessToken = new AccessToken();
            tokenIssuer.Exp = exp;
            tokenIssuer.Id = sub;
            tokenIssuer.AccessToken.Aud = aud;
            tokenIssuer.AccessToken.Iss = iss;
            tokenIssuer.AccessToken.Sub = sub;
            tokenIssuer.AccessToken.Jti = jti;
            tokenIssuer.AccessToken.Roles = roles;
            tokenIssuer.AccessToken.Exp = exp;
            return tokenIssuer;
        }
        
/* TODO: update user session
        1 Провалидировать токен
        1.1 получить информацию о секретном ключе Get запросом к http://static_data:8080/jwk/symmetric.json (поле k, получать его надо каждый раз (вдруг я его изменю?))
        1.2 Провалидировать подпись
        1.3 Провалидировать время жизни токена
        2 Из токена вытащить параметры (sub, jti, roles)
        2 Выдать новый токен (в открытом виде)

    curl -X PUT --data '{"access_token":"access.token.string"}' http://localhost:5000/api/v1/token
        {
            "access_token": {
                "aud": "https://api.lacmus.org",
                "iss": "https://api.lacmus",
                "sub": "1234567890qwertyuio",
                "jti": "mnb23vcsrt756yuiomnbvcx98ertyuiop",
                "roles": ["user", "admin"],
                "exp": 1735689600
            },
            "exp": 1735689600,
            "user_id": "1234567890qwertyuio"
        }
 */
        [HttpPut]
        public ActionResult<TokenIssuer> RefreshToken([FromBody] RefreshToken model)
        {
            string sub;
            string jti;
            List<string> roles;
            
            try
            {
                var token = Jose.JWT.Decode<AccessToken>(model.Token, Convert.FromBase64String("a2V5"));
                sub = token.Sub;
                jti = token.Jti;
                roles = token.Roles;
                Console.WriteLine("Token is valid!");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Invalid token: {e}");
                return Unauthorized();
            }
            
            UInt64 exp = 1735689600;
            var aud = "https://lacmus.io";
            var iss = "https://lacmus";
            
            var tokenIssuer = new TokenIssuer();
            tokenIssuer.AccessToken = new AccessToken();
            tokenIssuer.Exp = exp;
            tokenIssuer.Id = sub;
            tokenIssuer.AccessToken.Aud = aud;
            tokenIssuer.AccessToken.Iss = iss;
            tokenIssuer.AccessToken.Sub = sub;
            tokenIssuer.AccessToken.Jti = jti;
            tokenIssuer.AccessToken.Roles = roles;
            tokenIssuer.AccessToken.Exp = exp;
            return tokenIssuer;
        }
    }
}