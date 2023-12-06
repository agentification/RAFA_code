

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b d)
(on c g)
(on d c)
(on e a)
(ontable f)
(on g f)
(ontable h)
(on i e)
(clear b)
(clear i)
)
(:goal
(and
(on a h)
(on b i)
(on c d)
(on e f)
(on f a)
(on g c)
(on h b))
)
)


