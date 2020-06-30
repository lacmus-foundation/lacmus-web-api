using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;
using Identity.ViewModels.Login;

namespace Identity.ViewModels.UserLogin
{
    public class LoginViewModel : ILoginViewModel
    {
        [Required]
        [JsonPropertyName("email")]
        public string Email { get; set; }
        [Required]
        [JsonPropertyName("password")]
        public string Password { get; set; }
    }
}